# Simple static file server using HttpListener
$prefix = "http://localhost:8000/"
$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($prefix)
$listener.Start()
Write-Output "Serving $root at $prefix"

function Get-ContentType($ext){
  switch ($ext.ToLower()){
    '.html' { 'text/html; charset=utf-8' }
    '.htm'  { 'text/html; charset=utf-8' }
    '.js'   { 'application/javascript; charset=utf-8' }
    '.css'  { 'text/css; charset=utf-8' }
    '.json' { 'application/json; charset=utf-8' }
    '.png'  { 'image/png' }
    '.jpg'  { 'image/jpeg' }
    '.jpeg' { 'image/jpeg' }
    '.gif'  { 'image/gif' }
    '.svg'  { 'image/svg+xml' }
    '.webmanifest' { 'application/manifest+json' }
    default { 'application/octet-stream' }
  }
}

try{
  while ($listener.IsListening) {
    $context = $listener.GetContext()
    $req = $context.Request
    $resp = $context.Response
    $urlPath = [System.Uri]::UnescapeDataString($req.Url.AbsolutePath.TrimStart('/'))
    if ([string]::IsNullOrEmpty($urlPath)) { $urlPath = 'index.html' }
    $fsPath = Join-Path $root $urlPath
    if (Test-Path $fsPath -PathType Container) {
      $fsPath = Join-Path $fsPath 'index.html'
    }
    if (Test-Path $fsPath) {
      $bytes = [System.IO.File]::ReadAllBytes($fsPath)
      $ext = [System.IO.Path]::GetExtension($fsPath)
      $resp.ContentType = Get-ContentType $ext
      $resp.ContentLength64 = $bytes.Length
      $resp.AddHeader('Access-Control-Allow-Origin','*')
      $resp.OutputStream.Write($bytes,0,$bytes.Length)
    } else {
      $resp.StatusCode = 404
      $msg = "404 Not Found"
      $buf = [System.Text.Encoding]::UTF8.GetBytes($msg)
      $resp.ContentType = 'text/plain; charset=utf-8'
      $resp.ContentLength64 = $buf.Length
      $resp.OutputStream.Write($buf,0,$buf.Length)
    }
    $resp.OutputStream.Close()
  }
} catch {
  Write-Output "Server stopped: $_"
} finally {
  if ($listener -and $listener.IsListening) { $listener.Stop(); $listener.Close() }
}
