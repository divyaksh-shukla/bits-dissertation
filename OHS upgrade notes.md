# OHS Notes
*Forecasting Bangalore/General/Files/Learnings/OHS upgrade notes.md*
## Table of Contents
- [OHS Notes](#ohs-notes)
  - [Table of Contents](#table-of-contents)
  - [Steps to Upgrade (v2.2.0.1)](#steps-to-upgrade-v2201)
  - [OHS Machine (CC) `10.160.130.4`](#ohs-machine-cc-101601304)
  - [Data Connector VM `10.160.130.5`](#data-connector-vm-101601305)
  - [To be done (DONE and Tested)](#to-be-done-done-and-tested)
    - [Some other scenario](#some-other-scenario)
  - [SampleFile](#samplefile)
  - [Stage Deployment](#stage-deployment)
  - [Some parameters](#some-parameters)
  - [Errors](#errors)


## Steps to Upgrade (v2.2.0.1)
1)	OHS Installer link (version.: 2.2.0.1): [Get the latest version](https://urldefense.com/v3/__https:/dev.azure.com/itron/_apis/resources/Containers/4404326/OHS_Installer_Release?itemPath=OHS_Installer_Release*Itron.Platform.OHS_2.2.0.1.msi__;Lw!!F7jv3iA!nHq_ZuSD9BzCGbeDiRrga4AJ6YVlIUdko39PzxSucMxFiOeDfmvmsso786bZ_g4$) [Release Notes](https://itron.sharepoint.com/sites/SoftwarePlatform/ohsreleases/Lists/Posts/Post.aspx?ID=8)
> Copy and paste this if the link does not work 
> 
> `https://urldefense.com/v3/__https:/dev.azure.com/itron/_apis/resources/Containers/4404326/OHS_Installer_Release?itemPath=OHS_Installer_Release*Itron.Platform.OHS_2.2.0.1.msi__;Lw!!F7jv3iA!nHq_ZuSD9BzCGbeDiRrga4AJ6YVlIUdko39PzxSucMxFiOeDfmvmsso786bZ_g4$`
> 
> Relase Notes
> 
> `https://itron.sharepoint.com/sites/SoftwarePlatform/ohsreleases/Lists/Posts/Post.aspx?ID=8`

2)	Before installing OHS v2, take a backup (Copy) of the v1 folder  `C:\Program Files (x86)\Platform.HybridConnector`. In case installation went wrong or accidentally uninstalled v1,
backup folder will help us to get back these config files.
    - `C:\Program Files (x86)\Platform.HybridConnector\Itron.Cloud.Platform.HybridConnector.OHS.exe.config`
    - `C:\Program Files (x86)\Platform.HybridConnector\OnPremisesHybridService.json`
3) Stop the OHS v1 service. Go to `Services` in windows. Right click and stop the service `Itron On-Premises Hybrid Service`
4) Go to **`SharedFolder`** mentioned in `OnPremisesHybridService.json`  And delete the `Databases` Folder.
5) Click on the installer . While installing ,following setup window will come (after accepting 'terms and conditions'):
**Click on the Migrate tab.**
6) Migrate tab will show the config file path window as shown below. Configurations from previous version will be automatically selected in the file path.
**Click on Next.**
7) It will show a pop up window as shown below. **Click on Yes.**
8) **The OHS is installed successfully in the machine.**
9) After successful installation go to `Services` in windows. Right click and Start the service `Itron.Platform.OHS_2.2.0.1.` After that, the status should show as `Running`.
10) **The OHS v2 setup in client's machine is done.**


## OHS Machine (CC) `10.160.130.4`
- Features.json - `C:\\Program Files\\Platform.IHC\\Features.json`
  - contains download and upload file paths
  - Only has `ClientId` and `ClientSecret`, seems like `TenantId` is derived
  - to be changed after stopping the service `Itron.Platform.OHS_<version>`, run it back once the feature.json has been updated 
  - `ClientId`, `ClientSecret` and `Scope` will be provided by OHS team after our tenant is provisioned
- Logs - `C:\\temp\\OHSv2\\logs`
  - Search for errors here
  - Client side debugging
  - For checking real client side logs we can check OHS resource group for appinsights `ai-usw-ihc-prod`
- Files - `C:\\temp\\pickup`
  - Inside `<tenantId>` folder (automatically created by Features.json)
  - 2 folders in it
    - `file-downloads` - contains files which are uploaded from the other VM
    - `file uploads`
  - Put a dummy file in `file-uploads\\kpi-files` and this will be downloaded to Data Connector VM (MetrixIDR VM)

## Data Connector VM `10.160.130.5`
- Config file - `C:\\Program Files\\Itron\\DataConnector\\OnPremisesHybridConfiguration`
  - Has tenantId for each forecasting tenant
  - File upload and download paths
- Appsettings - `C:\\Program Files\\Itron\\DataConnector\\Itron.Cloud.Forecasting.BlobWinSvc.exe.config`
  - `ClientId`, `ClientSecret` and `Scope` to be changed for each customer
  - Can also configure log paths in here
- Service `Itron Forecasting DataConnector Service` has to be started after config modification
- Logs - `C:\\HybridConnectorLog\\HC-{Date}.txt`
- File upload and download
  - Upload - `C:\\HybridOnPremiseConnector\\Upload-files\\<tenantId>` - drop a file here to be uploaded to OHS VM
  - Download - `C:\\import\\FileDownload\\<tenantId>`
    - To be configured
- Settings-wise URL changes
  - Appsettings file `C:\\Program Files\\Itron\\DataConnector\\Itron.Cloud.Forecasting.BlobWinSvc.exe.config`
  - change the `IHCServiceUrl` from `v1` to `v2`
- Code-wise URL changes
  - PR [changed from v1 to v2](https://dev.azure.com/itron/CloudServicesPlatform/_git/Forecast.DataConnector/pullrequest/68024?_a=files)
  - In-short the config changes in appsettings is reflected in the code to hit the new URLs

## To be done (DONE and Tested)
- CC machine
    1) Start the service
- Data Connector Machine
    1) Start the service
    2) Upload a dummy file from here
    3) It should be successfully downloaded to CC machine
    4) If this works then everything is fine 
- [x] <span style="background-color: lightgreen">**Working**</span>
- To check failure
  - Connect to the Service Bus [sb-usw-frct-test2](https://portal.azure.com/#@itron.onmicrosoft.com/resource/subscriptions/9350e6db-d02d-4db7-baee-76f9498dfd13/resourceGroups/rgp-usw-fc-test2/providers/Microsoft.ServiceBus/namespaces/sb-usw-frcst-test2/overview)
  - Service Bus Connection String - `Endpoint=sb://sb-usw-frcst-test2.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=vHLsmOFuOfPqa9Jk8uDNbK4wqecljUUmVQVjCT9Y9ps=`

### Some other scenario
- [x] Working - CC machine in v1 while dataconnector machine in v2 to test backward compatibility

## SampleFile
Name: dshukla_20200511_115025.txt
```txt
Name,Data,Remark
Divyaksh,New data,Hello from the other side
```

## Stage Deployment
1) code deployment to stage
2) IHC service URL in config change to v2
3) Install OHSv2 MSI in cc machine (stage)  
```powershell
# v2.2.0.1 (latest)
wget https://forecastingstorageac.blob.core.windows.net/ohs/Itron.Platform.OHS_2.2.0.1.msi -OutFile Itron.Platform.OHS_2.2.0.1.msi  

# v2.1.0.48 (NOT WORKING)
wget https://dev.azure.com/itron/_apis/resources/Containers/3789824?itemPath=OHS_Installer_Release/Itron.Platform.OHS_2.1.0.48.msi -OutFile Itron.Platform.OHS_2.1.0.48.msi
```
4) take a back up of dataconnector service folder before triggering the release in stage inside the VM (`<C:<\\Program Files\\Itron\\DataConnector>>`)

## Some parameters
Test2
```json
{
"IdentityUrl": "https://idenservertest2.itrontotaltest.com/connect/token",
"Identityuserclientid": "c04bb2a1-9273-4b84-a094-abbcc7f0ee96",
"Identityuserclientsecret": "usercheck123",
"Identityusergranttype": "client_credentials",
"Identityuserscope": "forecastingscope",
}
{
  "MRES": "6c40ed2f-2b43-43ea-86ee-9e0f8e2eebd2"
}
```
Stage
```json
{
"IdentityUrl": "https://idenserver.itrontotalstage.com/connect/token",
"Identityuserclientid": "35875b30-0568-4e34-8c45-6662406ec0e6",
"Identityuserclientsecret": "frcstusr123",
"Identityusergranttype": "client_credentials",
"Identityuserscope": "forecastingscope",
},
{
"client id": "8397e8fd-58a8-4b1d-8ee0-f05a37d8cca8", 
"pass": "4csvMUYtyk2MkVJLGPW7FVf6Sq5QnyXU",
"scope": "HybridConnector"
}
```
Prod
```json
{
"IdentityUrl": "https://idenserver.itrontotal.com/connect/token",
"Identityuserclientid": "35875b30-0568-4e34-8c45-6662406ec0e6",
"Identityuserclientsecret": "frcstusr123",
"Identityusergranttype": "client_credentials",
"Identityuserscope": "forecastingscope",
}

TEST2: {

      IdentityUrl: "https://idenservertest2.itrontotaltest.com/connect/token",

      baseurl:

        "https://k8stest2.itrontotaltest.com/forecastadmingateway/api/v1/",

      headers: {

        ["correlationId"]: "73f709c6-2963-4351-8ec3-eecc6437f96e",

        ["Itron-CorrelationId"]: "183b8b69-f4b4-4235-831e-f9c432a96f8d",

        ["Content-Type"]: "application/x-www-form-urlencoded",

      },

      form: {

        ["client_id"]: "c04bb2a1-9273-4b84-a094-abbcc7f0ee96",

        ["client_secret"]: "usercheck123",

        ["scope"]: "forecastingscope",

        ["grant_type"]: "client_credentials",

      },

    },
```

## Errors
- [x] Fixed
```
[2020-04-28 09:20:41  DBG] POST request: https://idenservertest2.itrontotaltest.com/connect/token 
[2020-04-28 09:20:42  WRN] The remote name could not be resolved: 'idenservertest2.itrontotaltest.com'
 Http-status code: 0. Retry count '1' after timespan 00:00:00.2000000  
[2020-04-28 09:20:42  WRN] The remote name could not be resolved: 'idenservertest2.itrontotaltest.com'
```

```log
2020-05-11 10:50:20.856 +00:00 [Information] New file 'rouf.txt'  found for upload, count 27.
2020-05-11 10:50:20.856 +00:00 [Error] efaca90d-5525-4ebe-9bf9-3fd6cbc666fc
2020-05-11 10:50:20.856 +00:00 [Fatal] File upload failed for file rouf.txt  with associated tenant 35035eed-9b39-4d1a-8f2e-3575b27d009e<EventTag { correlationId: efaca90d-5525-4ebe-9bf9-3fd6cbc666fc, contentTypeId: fe6c9606-67d5-49bc-9363-c6006ed14ee6, tenantId: 35035eed-9b39-4d1a-8f2e-3575b27d009e, fileTransferEvent: SentFailed }
System.AggregateException: One or more errors occurred. ---> System.ArgumentNullException: Value cannot be null.
Parameter name: uriString
   at System.Uri..ctor(String uriString)
   at Itron.Cloud.Forecasting.BlobWinSvc.Common.SasToken.<GetSasUriForFileAsync>d__7.MoveNext()
   --- End of inner exception stack trace ---
   at System.Threading.Tasks.Task.ThrowIfExceptional(Boolean includeTaskCanceledExceptions)
   at System.Threading.Tasks.Task`1.GetResultCore(Boolean waitCompletionNotification)
   at System.Threading.Tasks.Task`1.get_Result()
   at Itron.Cloud.Forecasting.BlobWinSvc.FileUoloadService.OhsUploadService.<>c__DisplayClass20_0.<Scan>b__0(FileInfo f)
---> (Inner Exception #0) System.ArgumentNullException: Value cannot be null.
Parameter name: uriString
   at System.Uri..ctor(String uriString)
   at Itron.Cloud.Forecasting.BlobWinSvc.Common.SasToken.<GetSasUriForFileAsync>d__7.MoveNext()<---
2020-05-11 10:50:20.856 +00:00 [Information] New file 'rouf.txt'  found for upload, count 27.
2020-05-11 10:50:20.856 +00:00 [Error] efaca90d-5525-4ebe-9bf9-3fd6cbc666fc
2020-05-11 10:50:20.856 +00:00 [Fatal] File upload failed for file rouf.txt  with associated tenant 35035eed-9b39-4d1a-8f2e-3575b27d009e<EventTag { correlationId: efaca90d-5525-4ebe-9bf9-3fd6cbc666fc, contentTypeId: fe6c9606-67d5-49bc-9363-c6006ed14ee6, tenantId: 35035eed-9b39-4d1a-8f2e-3575b27d009e, fileTransferEvent: SentFailed }
System.AggregateException: One or more errors occurred. ---> System.ArgumentNullException: Value cannot be null.
Parameter name: uriString
   at System.Uri..ctor(String uriString)
   at Itron.Cloud.Forecasting.BlobWinSvc.Common.SasToken.<GetSasUriForFileAsync>d__7.MoveNext()
   --- End of inner exception stack trace ---
   at System.Threading.Tasks.Task.ThrowIfExceptional(Boolean includeTaskCanceledExceptions)
   at System.Threading.Tasks.Task`1.GetResultCore(Boolean waitCompletionNotification)
   at System.Threading.Tasks.Task`1.get_Result()
   at Itron.Cloud.Forecasting.BlobWinSvc.FileUoloadService.OhsUploadService.<>c__DisplayClass20_0.<Scan>b__0(FileInfo f)
---> (Inner Exception #0) System.ArgumentNullException: Value cannot be null.
Parameter name: uriString
   at System.Uri..ctor(String uriString)
   at Itron.Cloud.Forecasting.BlobWinSvc.Common.SasToken.<GetSasUriForFileAsync>d__7.MoveNext()<---

```

<!-- # Test2 OHS
- File upload and Download Request response
  - Features.json - `C:\Program Files\Platform.IHC\Features.json`
  - `ClientId`, `ClientSecret` and `ClientScope` are unchanged
- WCF request Response **Not Used**
```
{
    "Id": "<Instance Id>",
    "WorkspaceFolder": "C:\\Temp\\pickup",
    "Systems": [
        {
            "Id": "fbec52f4-0c3b-47dd-99af-1aefa2f2acdb",
            "SystemName": "OWOC-CM",
            "LongName": "OWOC-CM",
            "IsEnabled": true,
            "Tenants": [
                {
                    "IsEncrypted": false,
                    "ClientId": "<Client Id>",
                    "ClientSecret": "<Client secret>",
                    "ClientScope": "<Client scope>",
                    "RunOnPremises": null,
                    "RemoteRequest": {
                        "WcfConnections": [
                            {
                                "Id": "11cf7d84-9295-4811-ab0f-f40239327db3",
                                "BindingName": "basicBinding",
                                "BehaviorName": "DirectEndpoint",
                                "Uri": "http://localhost:8080",
                                "IsDefault": true,
                                "IsSecureConnection": false,
                                "HasWsHeader": false
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
``` -->


```json
"ClientId": "0455a398-adb3-4b80-a6b3-2a6dd2b103e4",
"ClientSecret": "hy9r16OHS",
"ClientScope": "HybridConnector",
```

```xml
<add key="clientId" value="d3790f06-aed2-4482-81c0-f722a2b84037" />

<add key="clientSecret" value="hy9r16OHS" />
<add key="Scope" value="HybridConnector" />
```