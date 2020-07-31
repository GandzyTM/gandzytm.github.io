<template>
  <div>
    <b-alert variant="success" show="10" dismissible @dismissed='showAlert'>{{message}}
    </b-alert>
  </div>
</template>

<script>
export default {
  props: ['message'],
  methods: {
    showAlert() {
      this.$emit('new_trigger');
    },
  },
};
</script>
