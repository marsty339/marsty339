build:build-darwin build-linux

build-darwin:
	CGO_ENABLED=0 GOOS=darwin GOARCH=amd64 go build -ldflags="-X master.Commit=$(git rev-parse HEAD)" -o alauda-fe-darwin-amd64 main.go
	CGO_ENABLED=0 GOOS=darwin GOARCH=arm64 go build -ldflags="-X master.Commit=$(git rev-parse HEAD)" -o alauda-fe-darwin-arm64 main.go

build-linux:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags="-X master.Commit=$(git rev-parse HEAD)" -o alauda-fe-linux-amd64 main.go
	CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -ldflags="-X master.Commit=$(git rev-parse HEAD)" -o alauda-fe-linux-arm64 main.go

clean:
	rm -rf alauda-fe-linux-amd64 alauda-fe-linux-arm64 alauda-fe-darwin-amd64 alauda-fe-darwin-arm64