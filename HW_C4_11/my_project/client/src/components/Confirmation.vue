<template>
  <div>
    <b-alert variant="success" show="10" dismissible @dismissed='showalert'>{{message}}
    </b-alert>
  </div>
</template>

<script>
export default {
  props: ['message'],
  methods: {
    showalert() {
      this.$emit('new_trigger');
    },
  },
};
</script>
