<script setup>
import { ref } from 'vue'
import api from '@/apiService'

const ticker = ref('')
const start = ref('')
const end = ref('')
const loading = ref(false)
const result = ref(null)
const error = ref(null)

const fetchCompany = async () => {
  error.value = null
  result.value = null
  loading.value = true
  try {
    const response = await api.post('fetch-company-data/', {
      ticker: ticker.value,
      start: start.value,
      end: end.value,
    })
    result.value = response.data
  } catch (e) {
    error.value = e?.response?.data?.error || e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card>
    <v-card-title>
      <v-icon class="me-2">mdi-magnify</v-icon>
      Search & Add Company from Yahoo Finance
    </v-card-title>
    <v-card-text>
      <v-form @submit.prevent="fetchCompany">
        <v-text-field v-model="ticker" label="Ticker (e.g. AAPL)" required />
        <v-row>
          <v-col>
            <v-text-field v-model="start" label="Start Date (YYYY-MM-DD)" required type="date" />
          </v-col>
          <v-col>
            <v-text-field v-model="end" label="End Date (YYYY-MM-DD)" required type="date" />
          </v-col>
        </v-row>
        <v-btn color="primary" type="submit" :loading="loading" :disabled="loading">
          Fetch Data
        </v-btn>
      </v-form>
      <v-alert v-if="result" type="success" class="mt-4" border="start" prominent>
        Company <b>{{ result.company.name }}</b> added.<br />
        Prices added: {{ result.prices_added }}<br />
        Prices skipped (already in DB): {{ result.prices_skipped }}
      </v-alert>
      <v-alert v-if="error" type="error" class="mt-4" border="start" prominent>
        {{ error }}
      </v-alert>
    </v-card-text>
  </v-card>
</template>
