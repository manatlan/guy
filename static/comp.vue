<template>
    <span>
        {{cpt}}
        <button @click="inc()">++</button>
    </span>
</template>
<script>
{
    data() {
        return {cpt:0};
    },
    methods: {
        inc() { this.cpt+=1; }
    }
}
</script>
<style scoped>
    :scope {padding:10px;background:yellow; border:1px solid black}
</style>
<style>
    body {padding:10px}
</style>