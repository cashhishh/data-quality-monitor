const BASE_URL = "https://data-quality-monitor-1.onrender.com";

export async function uploadDataset(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${BASE_URL}/datasets/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Upload failed");
  }

  return response.json();
}

export async function runQualityChecks(datasetId) {
  const response = await fetch(
    `${BASE_URL}/datasets/run-checks/${datasetId}`,
    { method: "POST" }
  );

  if (!response.ok) {
    throw new Error("Quality check failed");
  }

  return response.json();
}

export async function getLatestDataset() {
  const response = await fetch(`${BASE_URL}/datasets/latest`);

  if (!response.ok) {
    throw new Error("Failed to fetch latest dataset");
  }

  return response.json();
}

export async function fetchDashboardStats() {
  const response = await fetch(`${BASE_URL}/dashboard/summary`);

  if (!response.ok) {
    throw new Error("Failed to load dashboard stats");
  }

  return response.json();
}
