terraform {
  cloud {
    organization = "JPITCORP"

    workspaces {
      name = "cloudlflare-automation"
    }
  }
}