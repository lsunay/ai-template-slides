<template>
  <div class="upload-section">
    <h2>Generate Presentation</h2>
    
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="text-input">Paste your text content:</label>
        <textarea
          id="text-input"
          v-model="text"
          placeholder="Paste your article, report, blog post, or bullet list here..."
          rows="10"
          required
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="template-select">Template:</label>
          <select id="template-select" v-model="template" required>
            <option value="academic">Academic</option>
            <option value="pitch_deck">Pitch Deck</option>
            <option value="sales">Sales Presentation</option>
          </select>
        </div>

        <div class="form-group">
          <label for="model-select">AI Model:</label>
          <select id="model-select" v-model="model" required>
            <option value="openai">OpenAI GPT</option>
            <option value="ollama">Ollama (Local)</option>
            <option value="lmstudio">LM Studio (Local)</option>
          </select>
        </div>
      </div>

      <button type="submit" :disabled="loading" class="generate-btn">
        <span v-if="!loading">Generate Presentation</span>
        <span v-else>Generating...</span>
      </button>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { generatePresentation } from '../api';

const emit = defineEmits<{
  generate: [result: { presentationId: string; downloadUrl: string }];
}>();

const text = ref('');
const template = ref('academic');
const model = ref('openai');
const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
  loading.value = true;
  error.value = '';

  try {
    const result = await generatePresentation({
      text: text.value,
      template: template.value,
      model: model.value,
    });

    emit('generate', {
      presentationId: result.presentation_id,
      downloadUrl: result.download_url,
    });
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An error occurred';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.upload-section {
  background: #f8f9fa;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #003366;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #333;
}

textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
}

textarea:focus {
  outline: none;
  border-color: #003366;
}

select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  background: white;
}

select:focus {
  outline: none;
  border-color: #003366;
}

.generate-btn {
  background: #003366;
  color: white;
  padding: 0.75rem 2rem;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.generate-btn:hover:not(:disabled) {
  background: #002244;
}

.generate-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem;
  background: #fee;
  color: #c33;
  border-radius: 6px;
  border-left: 4px solid #c33;
}
</style>