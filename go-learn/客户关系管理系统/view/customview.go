package main

import (
	"fmt"
	"test/service"
	"test/custom"
)

type customView struct {
	key string
	loop bool
	customerService *service.CustomService
}
func (this *customView) list(){
	customers := this.customerService.List()
	fmt.Println("------客户列表------")
	fmt.Println("编号\t姓名\t年龄\t电话\t邮箱")
	for i:=0;i<len(customers);i++{
		fmt.Println(customers[i].GetInfo())
	}
}
func (this *customView) update() {
	fmt.Println("---请输入待修改客户编号(-1退出)---")
	fmt.Println("key:")
	key := -1
	fmt.Scanln(&key)
	if key == -1 {
		return
	}
	custom:=this.customerService.Get(key)
	name := custom.GetName()
	fmt.Printf("姓名(%v):",name)
	fmt.Scanln(&name)
	sex := custom.GetSex()
	fmt.Printf("性别(%v):",sex)
	fmt.Scanln(&sex)
	age := custom.GetAge()
	fmt.Printf("年龄(%v):",age)
	fmt.Scanln(&age)
	phone := custom.GetPhone()
	fmt.Printf("电话(%v):",phone)
	fmt.Scanln(&phone)
	mail := custom.GetMail()
	fmt.Printf("邮件(%v):",mail)
	fmt.Scanln(&mail)
	if this.customerService.Update(key,name,sex,age,phone,mail) {
		fmt.Println("---更新成功---")
	}else{
		fmt.Println("---更新失败---")
	}
}
func (this *customView) delete(){
	fmt.Println("---请输入待删除客户编号(-1退出)---")
	fmt.Println("key:")
	key:=-1
	fmt.Scanln(&key)
	if key == -1 {
		return
	}
	for {
		fmt.Println("确认是否删除(y/n)")
		choice:=""
		fmt.Scanln(&choice)
		if choice == "y" || choice == "Y" {
			if this.customerService.Findby(key) {
				fmt.Println("---删除成功---")
				break
			} else {
				fmt.Println("---删除失败---")
				break
			}
		}
	}
}
func (this *customView) add(){
	fmt.Println("---添加客户---")
	fmt.Println("name:")
	name :=""
	fmt.Scanln(&name)
	fmt.Println("sex:")
	sex := ""
	fmt.Scanln(&sex)
	fmt.Println("age:")
	age :=0
	fmt.Scanln(&age)
	fmt.Println("phone:")
	phone :=""
	fmt.Scanln(&phone)
	fmt.Println("email:")
	mail:=""
	fmt.Scanln(&mail)
	customer := custom.NewCustomAccount2(name,sex,age,phone,mail)
	if this.customerService.Add(customer) {
		fmt.Println("---添加完成---")
	}else{
		fmt.Println("---添加失败---")
	}
}

func ( this *customView) mainMenu(){
	for{
		fmt.Println("\n----------客户信息管理----------")
		fmt.Println("                1 添加客户")
		fmt.Println("                2 修改客户")
		fmt.Println("                3 删除客户")
		fmt.Println("                4 客户列表")
		fmt.Println("                5 退出")
		fmt.Println("please enter(1-5):")
		fmt.Scanln(&this.key)
		switch this.key {
		case "1":
			this.add()
		case "2":
			this.update()
		case "3":
			this.delete()
		case "4":
			this.list()
		default:
			fmt.Println("请输入正确的选项")
		}
		if !this.loop {
			break
		}
	}
}
func main(){
	cv := customView{
		key : "",
		loop : true,
	}
	cv.customerService = service.NewCustomService()
	cv.mainMenu()
}