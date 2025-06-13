<template>
  <div v-if="places.length" class="mt-6 space-y-4">
    <div
      v-for="place in places"
      :key="place.Place_Id"
      class="border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition"
    >
      <h2 class="text-lg font-semibold text-blue-600">
        {{ place.Place_Name }}
      </h2>
      <p class="text-sm text-gray-500">📍 {{ place.City }}</p>
      <p class="text-sm mt-1">
        ⭐ Rata-rata Rating: {{ place.Place_Ratings ? place.Place_Ratings.toFixed(2) : 'Belum ada' }}
      </p>
    </div>
  </div>
  <div v-else class="mt-6 text-gray-500">Tidak ada hasil.</div>
</template>

<script>
export default {
  props: ['places']
}
</script>
