<template>
  <div class="p-8 max-w-xl mx-auto">
    <h1 class="text-2xl font-bold mb-4">Sistem Rekomendasi Wisata Berdasarkan Lokasi atau Nama Tempat</h1>
    <InputForm @submit="fetchRecommendations" />
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
      recommendedPlaces: []
    }
  },
  methods: {
    async fetchRecommendations(keyword) {
      try {
        const res = await fetch(
          `http://127.0.0.1:8000/recommend/location?q=${encodeURIComponent(keyword)}&top_n=5`
        )
        const data = await res.json()
        this.recommendedPlaces = data
      } catch (err) {
        console.error('Gagal mengambil rekomendasi:', err)
        this.recommendedPlaces = []
      }
    }
  }
}
</script>
