/*
Copyright © 2022 NAME HERE <EMAIL ADDRESS>
*/
package cmd

import (
	"context"
	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
	"github.com/spf13/cobra"
	"log"
	"os"
)

var filename, filepath string

// rootCmd represents the base command when called without any subcommands
var rootCmd = &cobra.Command{
	Use:   "tsminio",
	Short: "a upload cli to minio",
	Long:  `upload tar file to minio`,
	Run: func(cmd *cobra.Command, args []string) {
		upload(filename, filepath)
	},
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		log.Fatal(err)
		os.Exit(-1)
	}
}

func init() {
	rootCmd.Flags().StringVarP(&filename, "filename", "f", "", "filename")
	rootCmd.Flags().StringVarP(&filepath, "filepath", "p", "", "filepath")
}

func upload(filename string, filepath string) {
	ctx := context.Background()
	endpoint := "192.168.186.12:9000"
	accessKeyID := "minioadmin"
	secretAccessKey := "minioadmin"
	useSSL := false
	minioClient, err := minio.New(endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(accessKeyID, secretAccessKey, ""),
		Secure: useSSL,
	})
	check(err)
	log.Printf("%#v\n", minioClient)
	bucketName := "asm-demo"
	var filePath string
	filePath = filepath + filename
	contentType := "application/x-compressed-tar"
	info, err := minioClient.FPutObject(ctx, bucketName, filename, filePath, minio.PutObjectOptions{ContentType: contentType})
	log.Printf("Successfully uploaded %s of size %d\n", filename, info.Size)
}
func check(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
