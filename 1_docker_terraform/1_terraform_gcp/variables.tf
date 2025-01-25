variable "credentials" {
    description = "My service account credential"
    default = "./my-keys.json"  
}

variable "projectId" {
  description = "Full project name-ID"
  default = "terraform-demo-448017"
}

variable "projectNumber" {
  description = "Project number"
  default = "117646567744"
}

variable "location" {
  description = "Default location/region as São Paulo"
  default = "southamerica-east1"
}

variable "bqDatasetName" {
  description = "Default name for the dataset"
  default =  "demo_dataset"
}