<template>
  <div id="app">
    <header>
      <h1>🤖 AI Template Slides</h1>
      <p>Transform your text into professional presentations</p>
    </header>

    <main>
      <UploadText @generate="handleGenerate" />
      
      <div v-if="presentation" class="result-section">
        <h2>Your Presentation is Ready!</h2>
        
        <div class="actions">
          <a 
            :href="downloadUrl" 
            download 
            class="download-btn"
          >
            📥 Download Presentation
          </a>
          
          <button 
            @click="showPreview = !showPreview" 
            class="preview-btn"
          >
            👁️ {{ showPreview ? 'Hide' : 'Show' }} Preview
          </button>
        </div>

        <div v-if="showPreview" class="preview-container">
          <iframe 
            :src="previewUrl" 
            width="100%" 
            height="600px" 
            frameborder="0"
          ></iframe>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import UploadText from './components/UploadText.vue';
import { getDownloadUrl, getPreviewUrl } from './api';

const presentation = ref<{ presentationId: string; downloadUrl: string } | null>(null);
const showPreview = ref(false);

const downloadUrl = computed(() => {
  if (!presentation.value) return '';
  return getDownloadUrl(presentation.value.presentationId);
});

const previewUrl = computed(() => {
  if (!presentation.value) return '';
  return getPreviewUrl(presentation.value.presentationId);
});

const handleGenerate = (result: { presentationId: string; downloadUrl: string }) => {
  presentation.value = result;
  showPreview.value = true;
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: #f5f7fa;
  color: #333;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

header {
  background: linear-gradient(135deg, #003366 0%, #0066cc 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

header p {
  font-size: 1.2rem;
  opacity: 0.9;
}

main {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  width: 100%;
}

.result-section {
  margin-top: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.result-section h2 {
  color: #003366;
  margin-bottom: 1.5rem;
}

.actions {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.download-btn, .preview-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  transition: all 0.2s;
}

.download-btn {
  background: #003366;
  color: white;
}

.download-btn:hover {
  background: #002244;
}

.preview-btn {
  background: #6c757d;
  color: white;
}

.preview-btn:hover {
  background: #5a6268;
}

.preview-container {
  border: 2px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .actions {
    flex-direction: column;
  }
  
  header h1 {
    font-size: 2rem;
  }
}
</style>