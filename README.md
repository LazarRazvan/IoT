# Smart-Heating

This repository provides a comprehensive guide on how to interact with Huawei Fusion Solar devices and Tuya Smart devices through their respective APIs. Whether you are a developer looking to integrate these devices into your applications or a curious user interested in exploring the capabilities of your Huawei Fusion Solar or Tuya Smart devices, this repository aims to cover the requests.

## Introduction

Huawei Fusion Solar is a cutting-edge solution for solar energy management, while Tuya Smart devices provide smart home automation capabilities. This repository aims to bridge the gap between developers and these devices by offering documentation, code samples, and best practices for integrating them into your projects.

## Prerequisites

### Huawei Fusion Solar OpenAPI

Huawei Fusion Solar enables device interaction through an [Open API](https://forum.huawei.com/enterprise/en/communicate-with-fusionsolar-through-an-openapi-account/thread/667232424741978112-667213868771979264) account.

- if you don't already have an Open API account, you can find a comprehensive guide on creating one at the following [link](https://forum.huawei.com/enterprise/en/smart-pv-encyclopedia-how-to-create-a-northbound-api-account-through-the-fusionsolar/thread/667272196474683392-667213868771979264).

### Tuya IoT

The [Tuya IoT Development Platform](https://iot.tuya.com/) is an ecosystem dedicated to connect smart devices efficiently and securely.

- if you don't already have an Tuya IoT account, you can find a comprehensive guide on creating and linking smart devices at the following [link](https://developer.tuya.com/en/docs/iot/link-devices?id=Ka471nu1sfmkl)

## Implementation

### HuaweiFusionSolar Methods
- login
- logout
- plant_list
- plant_real_time_data
- plant_hourly_data
- plant_daily_data
- plant_monthly_data
- plant_yearly_data
- device_list
- device_real_time_data
- device_history_data
- device_daily_data
- device_monthly_data
- device_yearly_data

### HuaweiInverter Methods
- real_time_data
- daily_data
- monthly_data
- yearly_data
- real_time_active_power

### TuyaCloud
- command
- refresh_access_token
- get_devices
- get_device_status
- print_devices

### TuyaSwitch
- turn_on
- turn_off
- turn_custom
- get_status

## Examples
TODO

## Scenarios
TODO
