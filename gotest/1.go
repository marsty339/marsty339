package main

import (
	"fmt"
)



func main() {
	
	var a = [...]int{98,3,24,5,6,1}
	for i:=1;i<len(a);i++{
		
		if a[i-1]<a[i] {
			tmp := a[i-1]
			a[i-1]= a[i]
			a[i] = tmp
		}

	}
	fmt.Println(a)
	b := a[2:3]
	b[0] = 10
	fmt.Println(b,cap(b))

	
	b = append(b,1,1,1,1,1)
	fmt.Println(b,cap(b))

	fmt.Println(a)
}  
