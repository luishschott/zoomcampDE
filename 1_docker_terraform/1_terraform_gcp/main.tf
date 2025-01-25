terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.16.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project = var.projectId
  region = var.location
}

resource "google_bigquery_dataset" "demo-dataset" {
  dataset_id                  = var.bqDatasetName
  location                    = var.location

}

resource "google_storage_bucket" "demo-bucket" {
  name          = "terraform-demo-448017-demo-bucket"
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}