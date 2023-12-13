package main

import (
	"strings"
)

// AReader 实现了 io.Reader 接口，产生一个 'A' 的无限流
type AReader struct{}

// Read 实现了 io.Reader 接口的 Read 方法
func (r *AReader) Read(p []byte) (n int, err error) {
	// 将 'A' 复制到 p 中，重复利用 strings.Repeat()
	s := strings.Repeat("A", len(p))

	// 将 s 复制到 p 中
	n = copy(p, s)
	return n, nil
}

func main() {
	// 创建一个 AReader 实例
	reader := &AReader{}

	// 读取并输出前 10 个字符
	buffer := make([]byte, 10)
	n, err := reader.Read(buffer)
	if err != nil {
		panic(err)
	}

	// 输出读取的内容
	println(string(buffer[:n]))
}
