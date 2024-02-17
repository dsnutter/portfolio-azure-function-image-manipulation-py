$env:name_container = "fn_image_manipulation"
$env:version = "v2"
$env:tag = $env:name_container + ":" + $env:version
$env:ports = "8080:80"
$env:dockerfilePath = "../../dockerfiles/local-Dockerfile"

Write-Output "Building Container: $env:tag with dockerfile from $env:dockerfilePath"

docker build -f $env:dockerfilePath --tag $env:tag ../../azure_fn_image_manipulation/.

Write-Output "Running Container: $env:tag on port $env:ports"

$env:container_id = docker run -d -p $env:ports $env:tag

# Display the Docker container ID
Write-Output "Container ID: $env:container_id"
Write-Output "Container Tag: $env:tag"

$env:logfile = "current_$env:container_id.log"

docker logs $env:container_id > $env:logfile

Write-Output "Logfile for deploy is at $env:logfile"

docker ps
