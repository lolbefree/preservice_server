import-module activedirectory
$user =  $env:username
$comp = Get-ADUser $user  -properties labelcomputer | select -ExpandProperty labelcomputer
$comp