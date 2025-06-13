<template>
  <div class="container py-5">
    <div class="text-center mb-4">
      <h1 class="fw-bold display-6 text-primary">🌍 Sistem Rekomendasi Wisata</h1>
      <p class="text-muted fs-6">Temukan destinasi terbaik berdasarkan lokasi atau kata kunci</p>
    </div>

    <InputForm @submit="fetchRecommendations" />

    <div v-if="isLoading" class="text-center text-secondary mt-3">🔄 Memuat rekomendasi...</div>
    <div v-if="errorMessage" class="alert alert-danger mt-3">{{ errorMessage }}</div>

    <RecommendationList :places="recommendedPlaces" />
  </div>
</template>

<script>
import InputForm from './components/InputForm.vue'
import RecommendationList from './components/RecommendationList.vue'

export default {
  components: { InputForm, RecommendationList },
  data() {
    return {
      recommendedPlaces: [],
      isLoading: false,
      errorMessage: ''
    }
  },
  methods: {
  async fetchRecommendations(keyword) {
    this.isLoading = true
    this.errorMessage = ''
    this.recommendedPlaces = []

    try {
      const encoded = encodeURIComponent(keyword.trim())
      const res = await fetch(`http://localhost:8000/recommend/location?q=${encoded}&top_n=5`)
      if (!res.ok) throw new Error('Respon tidak OK')
      const data = await res.json()

      // ✅ Data sukses → hapus error dan tampilkan hasil
      this.recommendedPlaces = data
      this.errorMessage = ''   // <— Tambahkan ini
    } catch (err) {
      console.error('Gagal mengambil rekomendasi:', err)
      this.errorMessage = 'Gagal mengambil data. Coba lagi.'
      this.recommendedPlaces = []
    } finally {
      this.isLoading = false
    }
  }
}

}
</script>
