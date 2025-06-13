<template>
  <div class="p-8 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Sistem Rekomendasi Wisata Berdasarkan User ID</h1>
    <InputForm @submit="fetchRecommendations" />
    <p v-if="isLoading">🔄 Memuat rekomendasi...</p>
    <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>
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
    async fetchRecommendations(userId) {
      this.isLoading = true
      this.errorMessage = ''
      try {
        const res = await fetch("http://localhost:8000/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: userId, top_n: 5 })
        })
        const data = await res.json()
        this.recommendedPlaces = data
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
