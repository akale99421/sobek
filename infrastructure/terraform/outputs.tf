output "kubernetes_cluster_name" {
  value       = google_container_cluster.primary.name
  description = "GKE Cluster Name"
}

output "kubernetes_cluster_host" {
  value       = google_container_cluster.primary.endpoint
  description = "GKE Cluster Host"
  sensitive   = true
}

output "region" {
  value       = var.region
  description = "GCP region"
}

output "artifact_registry_repository" {
  value       = google_artifact_registry_repository.docker_repo.name
  description = "Artifact Registry Repository Name"
}

output "static_ip_address" {
  value       = google_compute_global_address.default.address
  description = "Static IP address for the application"
}

