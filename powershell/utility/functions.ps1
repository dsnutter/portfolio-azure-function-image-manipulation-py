function ConvertImageToBase64 {
    param(
        [string]$imagePath
    )

    $image = [System.IO.File]::ReadAllBytes($imagePath)
    $base64 = [System.Convert]::ToBase64String($image)

    return $base64
}

function ConvertBase64ToImage {
    param(
        [string]$base64File,
        [string]$outputPath
    )

    $base64 = Get-Content $base64File
    $image = [System.Convert]::FromBase64String($base64)
    [System.IO.File]::WriteAllBytes($outputPath, $image)
}

function CallImageApiJson {
    param(
        [string]$url,
        # body is hashtable
        [hashtable]$body,
        # azure function security key
        [string]$security_key
    )
    $method = "POST"

    $headers = @{
        "Content-Type" = "application/json"
        "x-functions-key" = "$security_key"
    }
    $json = $body | ConvertTo-Json

    $response = Invoke-RestMethod -Uri $url -Method $method -Headers $headers -Body $json
    return $response
}

function CallImageApiMultiPart {
    param(
        [string]$url,
        # form data is a hashtable
        [System.Collections.Hashtable]$formData,
        # azure function security key
        [string]$security_key
    )
    $method = "POST"

    $headers = @{
        "x-functions-key" = "$security_key"
    }

    $response = Invoke-RestMethod -Uri $url -ContentType "multipart/form-data" -Method $method -Headers $headers -Form $formData
    return $response
}

function GetImageDimensions_ViaMultiPart {
    param(
        [string]$imageFile,
        [string]$url,
        [string]$security_key
    )

    Write-Host "Getting image dimensions from api via multipart/form-data"
    Write-Host "for image: $imageFile"
    $file = Get-Item -Path $imageFile  
    
    # create form data
    $formData = @{
        image = $file 
    }
    
    try 
    {
        # call api
        $response = CallImageApiMultiPart $url $formData $security_key
        # $json_response = $response | ConvertTo-Json
        
        # parse response
        $width = $response.dimensions.width
        $height = $response.dimensions.height

        return $width, $height
    }
    catch 
    {
        Write-Host "Error calling api: $url"
        Write-Host "Is the endpoint running? Is the security key correct?"
        Write-Host "Error is: $_"
    }   
}


function GetImageDimensions_ViaJson {
    param(
        [string]$imageFile,
        [string]$url,
        [string]$security_key
    )

    Write-Host "Getting image dimensions from api via JSON"
    Write-Host "for image: $imageFile"
    $file = ConvertImageToBase64 $imageFile
    
    # create form data
    $body = @{
        image = $file 
    }
    
    try 
    {
        # call api
        $response = CallImageApiJson $url $body $security_key
        # $json_response = $response | ConvertTo-Json
        
        # parse response
        $width = $response.dimensions.width
        $height = $response.dimensions.height

        return $width, $height
    }
    catch 
    {
        Write-Host "Error calling api: $url"
        Write-Host "Is the endpoint running? Is the security key correct?"
        Write-Host "Error is: $_"
    }   
}