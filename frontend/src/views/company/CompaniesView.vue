<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api/apiService'

const companies = ref([])
const loading = ref(true)
const router = useRouter()

onMounted(async () => {
  try {
    const res = await api.get('companies/')
    companies.value = res.data
  } catch (err) {
    console.error('Error fetching companies:', err)
  } finally {
    loading.value = false
  }
})

const headers = [
  { title: 'Actions', value: 'actions', sortable: false },
  { title: 'Ticker', value: 'ticker' },
  { title: 'Name', value: 'name' },
  { title: 'ISIN', value: 'isin' },
  { title: 'Country', value: 'country' },
  { title: 'Sector', value: 'sector' },
  { title: 'Industry', value: 'industry' },
]
</script>

<template>
  <v-card>
    <v-card-title>
      <v-icon class="me-2">mdi-domain</v-icon>
      Companies
    </v-card-title>
    <v-card-text>
      <v-data-table
        :headers="headers"
        :items="companies"
        :loading="loading"
        loading-text="Loading companies..."
        class="elevation-1"
        item-value="id"
      >
        <template #item.name="{ item }">
          <strong>{{ item.name }}</strong>
        </template>

        <template #item.actions="{ item }">
          <v-btn
            density="compact"
            icon="mdi-information"
            :title="`Show details for ${item.name}`"
            @click="router.push(`/company/${item.ticker}`)"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
