const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface GenerateRequest {
  text: string;
  template: string;
  model: string;
}

export interface GenerateResponse {
  success: boolean;
  message: string;
  presentation_id: string;
  download_url: string;
}

export interface Template {
  name: string;
  description: string;
  display_name: string;
}

export interface Model {
  name: string;
  description: string;
  available: boolean;
}

export async function generatePresentation(data: GenerateRequest): Promise<GenerateResponse> {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to generate presentation');
  }

  return response.json();
}

export async function getTemplates(): Promise<Template[]> {
  const response = await fetch(`${API_BASE_URL}/templates`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch templates');
  }

  const data = await response.json();
  return data.templates;
}

export async function getModels(): Promise<Model[]> {
  const response = await fetch(`${API_BASE_URL}/models`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch models');
  }

  const data = await response.json();
  return data.models;
}

export function getDownloadUrl(presentationId: string): string {
  return `${API_BASE_URL}/download/${presentationId}`;
}

export function getPreviewUrl(presentationId: string): string {
  const downloadUrl = getDownloadUrl(presentationId);
  return `https://view.officeapps.live.com/op/embed.aspx?src=${encodeURIComponent(downloadUrl)}`;
}