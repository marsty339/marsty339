package main

import (
	"fmt"
	"net"
	"os"
)

func main() {
	ip, hostname := getIPAndHostname()
	fmt.Println(ip, hostname)
}
func getIPAndHostname() (string, string) {
	host, _ := os.Hostname()
	addrs, _ := net.LookupIP(host)
	var ip string
	for _, addr := range addrs {
		if ipv4 := addr.To4(); ipv4 != nil {
			ip = ipv4.String()
			break
		}
	}
	return ip, host
}
