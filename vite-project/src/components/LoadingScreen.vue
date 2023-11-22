<template>
  <div class="container">
    <div class="ring"></div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 8rem);
}

.ring {
  display: inline-block;
  width: 4rem;
  height: 4rem;
}

.ring:after {
  content: " ";

  box-sizing: border-box;

  display: block;
  width: 100%;
  height: 100%;

  border-radius: 50%;
  border-width: 0.3rem;
  border-style: solid;
  border-color: #ddd transparent #ddd transparent;

  animation: infinite-rotate 0.8s linear infinite;
}

@keyframes infinite-rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>
