<template>
    <v-container fluid class="py-4">
      <v-row>
        <v-col cols="12" lg="7">
          <!-- Karta z informacjami o spółce -->
          <v-card class="mb-4" elevation="2">
            <v-card-title class="text-h5">
              <v-icon class="me-2">mdi-domain</v-icon>
              {{ company.name }}
              <span class="ms-2 text-grey text-body-2">({{ company.ticker }})</span>
            </v-card-title>
            <v-divider />
            <v-card-text>
              <v-row>
                <v-col cols="12" sm="6" md="4">
                  <strong>ISIN:</strong> {{ company.isin || '–' }}
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <strong>Country:</strong> {{ company.country || '–' }}
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <strong>Sector:</strong> {{ company.sector || '–' }}
                </v-col>
                <v-col cols="12" sm="6" md="4">
                  <strong>Industry:</strong> {{ company.industry || '–' }}
                </v-col>
                <v-col cols="12" md="12" class="pt-2">
                  <strong>Description:</strong>
                  <div class="text-grey text-body-2" style="white-space: pre-line;">
                    {{ company.description || 'No description available.' }}
                  </div>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" lg="5">
          <v-card elevation="2">
            <v-card-title class="text-h6">
              <v-icon class="me-2">mdi-chart-line</v-icon>
              Price Chart
            </v-card-title>
            <v-divider />
            <v-card-text>
              <!-- Loader -->
              <div v-if="loading" class="d-flex justify-center my-6">
                <v-progress-circular indeterminate color="primary" size="48" />
              </div>
              <!-- Error alert -->
              <v-alert v-if="error" type="error" class="my-4">
                {{ error }}
              </v-alert>
              <!-- Wykres, gdy są dane -->
              <apexchart
                v-if="!loading && !error && series.length && options.xaxis.categories.length"
                type="line"
                height="300"
                :options="options"
                :series="series"
              />
              <div v-else-if="!loading && !error" class="text-center text-grey">
                <small>No price data to display.</small>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import { useTheme } from 'vuetify'
  import api from '@/api/apiService'
  
  const route = useRoute()
  const company = ref({})
  const series = ref([])
  const loading = ref(true)
  const error = ref(null)
  
  // ---- Motyw Vuetify ----
  const theme = useTheme()
  const isDark = ref(theme.global.current.value.dark)
  watch(
    () => theme.global.current.value.dark,
    (val) => {
      isDark.value = val
      setChartOptions()
    }
  )
  
  // ---- Opcje ApexCharts z automatycznym kolorem labeli ----
  const options = ref({})
  
  function setChartOptions() {
    const labelColor = isDark.value ? '#bdbdbd' : '#222'
    const bgColor = isDark.value ? '#181818' : '#fff'
    options.value = {
      chart: { id: 'price-line', background: bgColor },
      theme: { mode: isDark.value ? 'dark' : 'light' },
      xaxis: {
        categories: options.value.xaxis?.categories ?? [],
        labels: {
          style: {
            colors: labelColor,
            fontSize: '13px',
            fontFamily: 'Roboto, Arial, sans-serif',
            fontWeight: 400,
          }
        }
      },
      yaxis: {
        labels: {
          style: {
            colors: labelColor,
            fontSize: '13px',
            fontFamily: 'Roboto, Arial, sans-serif',
            fontWeight: 400,
          }
        }
      }
    }
  }
  
  // ---- Pobieranie danych ----
  onMounted(async () => {
    loading.value = true
    error.value = null
    try {
      const ticker = route.params.ticker
      const resCompany = await api.get(`company/${ticker}/`)
      company.value = resCompany.data
  
      const resPrices = await api.get(`company/${ticker}/prices/`)
      const prices = resPrices.data
      if (prices.length) {
        series.value = [
          {
            name: 'Close price',
            data: prices.map((row) => row.close),
          },
        ]
        // Ustawiamy dane do opcji wykresu
        options.value.xaxis = {
          ...(options.value.xaxis || {}),
          categories: prices.map((row) => row.date),
        }
      } else {
        series.value = []
        options.value.xaxis = { categories: [] }
      }
      setChartOptions()
    } catch (e) {
      error.value = e?.response?.data?.error || e.message
    } finally {
      loading.value = false
    }
  })
  </script>
  