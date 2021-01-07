package service

import (
	"test/custom"
)

type CustomService struct {
	customs []custom.CustomAccount
	customNum int
}
func NewCustomService() *CustomService {
	customservice := &CustomService{}
	customservice.customNum = 1
	customer := custom.NewCustomAccount(1,"张三","男",20,"112","wow@asiainfo.com")
	customservice.customs = append(customservice.customs,customer)
	return customservice
}

func (this *CustomService) List() []custom.CustomAccount {
	return this.customs
}
func (this *CustomService) Update( key int,name string,sex string,age int,phone string,mail string) bool {
	var custom = this.Get(key)
	custom.SetSex(sex)
	custom.SetName(name)
	custom.SetPhone(phone)
	custom.SetMail(mail)
	custom.SetAge(age)
	return true
}

func (this *CustomService) Get(key int) *custom.CustomAccount{
	var result *custom.CustomAccount
	for i:=0;i<len(this.customs);i++{
		if key == this.customs[i].GetId() {
			      result = &this.customs[i]
		}
	}
	return result
}


func (this *CustomService) Findby( key int)  bool{
	var result bool
	for i:=0;i<len(this.customs);i++{
			if key == this.customs[i].GetId() {
				this.customs = append(this.customs[:i],this.customs[i+1:]...)
				result =  true
			}else {
				result = false
			}
	}
	return result
}
func (this *CustomService) Add(customer  custom.CustomAccount) bool{
	this.customNum++
	customer.SetId(this.customNum)
	this.customs = append(this.customs,customer)
	return true
}