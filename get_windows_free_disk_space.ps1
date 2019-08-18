Windows Powershell Script

$disks = Get-WmiObject -Query "Select * from Win32_LogicalDisk"
$driveName = "C:"
$driveID = "Test"

foreach($disk in $disks)
    { 
      If ($disk.Name -eq $driveName ) {
      
        '{"values": {"": {"'+ $driveID + '":' + $disk.FreeSpace + '}}, "events": []}'
      }
    }

*********************************************************************************************************
# Array: Create Loop to list partitons and drives on system

$seed_class = @("Win32_LogicalDisk","Win32_DiskDrive","Win32_DiskDriveToDiskPartition","Win32_LogicalDiskToPartition","Win32_DiskPartition");
$Computer = "10.111.32.223" ; $Domain = "MYDOMAIN.COM" ; $Credential = Get-Credential ;   Invoke-Command -ScriptBlock {  Write-Host "*********************"; foreach ($item in $seed_class) { Get-WmiObject -Authority "ntlmdomain:$Domain" -Locale "MS_409" -Namespace "root\cimv2"  -ComputerName $Computer -Credential $Credential -Query "Select * from $item";  Write-Host "---------------------" }; Write-Host "*********************"  }
