package custom

import (
	"fmt"
)

type CustomAccount struct {
	id int
	name string
	sex string
	age int
	phone string
	mail string

}

func (this CustomAccount) GetInfo() string {
	info:=fmt.Sprintf("%v\t%v\t%v\t%v\t%v\t%v\t",this.id,
	this.name,this.sex,this.age,this.phone,this.mail)
	return info
}
func (this *CustomAccount) GetName() string{
	return this.name
}
func (this *CustomAccount) GetSex() string{
	return this.sex
}
func (this *CustomAccount) GetAge() int {
	return this.age
}
func (this *CustomAccount) GetPhone() string {
	return this.phone
}
func (this *CustomAccount) GetMail() string {
	return this.mail
}

func (this *CustomAccount) SetName(name string){
	this.name = name
}
func (this *CustomAccount) SetSex(sex string){
      this.sex = sex
}
func (this *CustomAccount) SetAge(age int){
	this.age = age
}
func (this *CustomAccount) SetPhone(phone string){
	this.phone = phone
}
func (this *CustomAccount) SetMail(mail string){
	this.mail = mail
}

func (this *CustomAccount) GetId() int {
	return this.id
}
func (this *CustomAccount) SetId(id int){
	this.id = id
}
func NewCustomAccount(id int, name string,sex string,age int,phone string,mail string) CustomAccount {
	return CustomAccount{
	id:id,
	name: name,
	sex: sex,
	age: age,
	phone: phone,
	mail: mail,
	}
}
func NewCustomAccount2( name string,sex string,age int,phone string,mail string) CustomAccount {
	return CustomAccount{
		name: name,
		sex: sex,
		age: age,
		phone: phone,
		mail: mail,
	}
}


