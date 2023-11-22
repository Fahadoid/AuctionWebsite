<script lang="ts" setup>
import { useRoute } from 'vue-router';
import { Ref, ref, onMounted } from 'vue';
import * as Api from '@/lib/api';
import { Item, ItemQuery, User } from '@/lib/api';
import LoadingScreen from '@/components/LoadingScreen.vue';
import DefaultIcon from '@/components/DefaultIcon.vue';

const route = useRoute();

const itemId = typeof route.params.id === 'string' ? parseInt(route.params.id) : parseInt(route.params.id[0]);

const item: Ref<Item | null> = ref(null);
const queries: Ref<ItemQuery[]> = ref([]);
const currentUser: Ref<User | null> = ref(null);

onMounted(async () => {
  // Make API requests without waiting for completion
  const itemPromise = Api.getItem(itemId);
  const queriesPromise = Api.getItemQueries(itemId);
  const userPromise = Api.getCurrentUser();

  // Now wait for completion
  item.value = await itemPromise;
  queries.value = await queriesPromise;
  currentUser.value = await userPromise;
});

const question: Ref<string> = ref('');

async function submitQuestion() {
  const questionText = question.value;
  // don't submit if the question is empty
  if (questionText.trim().length == 0) return;

  // Clear question to make the textarea empty
  question.value = '';

  const query = await Api.createItemQuery(itemId, {
    question: questionText,
  });
  queries.value.push(query);
}

const bidPopupVisible: Ref<boolean> = ref(false);
const bid: Ref<number> = ref(0);

function toggleBidPopup() {
  bidPopupVisible.value = !bidPopupVisible.value;
}

async function bidItem() {
  if (item.value === null) return;

  const currentPrice = parseFloat(item.value.current_price);
  // don't proceed unless bid is higher than current price
  if (bid.value <= currentPrice) return;

  bidPopupVisible.value = false;

  item.value = await Api.bidItem(item.value.id, { bid_price: bid.value });
}

const answer: Ref<string> = ref('');
const answerQueryId: Ref<number> = ref(0);
const answerFormVisible: Ref<boolean> = ref(false);

async function answerQuery() {
  answerFormVisible.value = false;
  await Api.answerItemQuery(itemId, answerQueryId.value, {
    answer: answer.value,
  });
  queries.value = await Api.getItemQueries(itemId);
}

async function showAnswerForm(id: number) {
  answerQueryId.value = id;
  answerFormVisible.value = true;
}
</script>

<template>
  <template v-if="item && queries && currentUser">
    <div class="details">
      <DefaultIcon class="photo" :obj="item" attr="photo_path" :alt="item.title" />
      <div>
        <div class="title">{{ item.title }}</div>
        <div class="description">{{ item.desc }}</div>
        <div class="price-info-container">
          <div class="price-info">
            <span class="label">Price: </span>
            <span class="price">£{{ item.current_price }}</span>
          </div>
          <button id="bid-popup-toggle" @click="toggleBidPopup" v-if="item.owner.id !== currentUser.id && !item.has_ended">Bid...</button>
        </div>
        <div class="bid-window" v-if="bidPopupVisible && !item.has_ended">
          <form id="bid-form">
            <label class="label" for="bid">Please enter a bid:</label>
            <div class="bid-price">
              <span class="currency">£</span>
              <input type="number" id="bid" :min="parseFloat(item.current_price) + 0.01" step="0.01" v-model="bid"
                :placeholder="(parseFloat(item.current_price) + 0.01).toFixed(2)" required>
            </div>
            <button type="submit" @click="bidItem">Bid</button>
          </form>
        </div>
        <div class="time-info">
          <span class="label">{{ item.has_ended ? 'Ended at: ' : 'Ends at: ' }}</span>
          <span class="time">{{ item.end_date }}</span>
        </div>
        <div class="bidder-info" v-if="item.bid_user">
          <span class="label">Bid by: </span>
          <span class="bidder">{{ item.bid_user.email }}</span>
        </div>
        <div class="seller-info">
          <span class="label">Sold by: </span>
          <span class="seller">{{ item.owner.email }}</span>
        </div>
        <div v-if="item.owner.id === currentUser.id" class="owner-actions">
          <router-link :to="`/change_items/${itemId}`">Edit Item</router-link>
        </div>
      </div>
    </div>
    <div class="queries">
      <h3>Questions ({{ queries.length }})</h3>
      <ul v-if="queries.length > 0" class="queries">
        <li v-for="q in queries" class="query">
          <p class="question">{{ q.question }}</p>
          <p class="answer">
            <template v-if="q.answer">
              {{ q.answer }}
            </template>
            <i v-else class="not-answered">(Not yet answered)</i>
          </p>
          <div v-if="item.owner.id == currentUser.id">
            <button type="submit" @click="showAnswerForm(q.id)">Answer</button>
          </div>
        </li>
      </ul>
      <div v-else style="margin: 1rem 0;">
        <i>No questions yet!</i>
      </div>
      <div>
        <form id="question-form">
          <label for="question">Ask a question:</label>
          <textarea v-model="question" col="5" placeholder="Your question here..." />
          <button type="submit" @click.prevent="submitQuestion">Submit</button>
        </form>
      </div>
      <div v-if="answerFormVisible">
        <div v-if="item.owner.id == currentUser.id">
          <form id="answer-form">
            <label for="answer">Answer a question:</label>
            <textarea v-model="answer" col="5" placeholder="Your answer here..." />
            <button type="submit" @click="answerQuery">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  <LoadingScreen v-else />
</template>

<style scoped>
.details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

@media (max-width: 800px) {
  .details {
    grid-template-columns: 1fr 1.4fr;
  }
}

@media (max-width: 520px) {
  .details {
    grid-template-columns: 1fr;
  }
}

.photo {
  border: black solid 1px;
  width: 100%;
  aspect-ratio: 1;
  object-fit: contain;
}

.title {
  color: black;
  font-weight: bold;
  font-size: 1.1rem;
  margin-bottom: 0.2rem;
}

.price-info {
  display: flex;
  flex-direction: row;
  align-items: baseline;

  font-size: 3rem;
}

.price-info > .label {
  font-size: 0.9rem;
}

.price-info-container {
  margin-top: 3rem;
  margin-bottom: 0.5rem;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}

#bid-popup-toggle {
  font-size: 1rem;
  /* position: absolute;
  right: 0;
  bottom: 0; */
}

.time-info {
  margin-bottom: 2rem;
  font-size: 0.9rem;
}

.bidder-info {
  font-size: 0.8rem;
  opacity: 0.6;
}

.seller-info {
  font-size: 0.8rem;
  opacity: 0.6;
}

.owner-actions {
  margin-top: 0.5rem;
  border-top: 1px solid #aaa;
  padding-top: 0.5rem;
}

.queries {
  display: block;
  padding: unset;
}

.query {
  list-style: none;
  border: 1px solid black;
  border-radius: 0.15rem;
  margin-bottom: 1rem;
}

.query:last-of-type {
  margin-bottom: 0;
}

.question::before {
  content: "Q: ";
  font-weight: bold;
}

.answer::before {
  content: "A: ";
  font-weight: bold;
}

.question {
  margin: 0.5rem 1rem;
}

.answer {
  margin: 0.5rem 1rem;
}

.not-answered {
  color: #aaa;
}

#question-form > label {
  display: block;
  font-weight: bold;
}

#question-form > textarea {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  display: block;
  box-sizing: border-box;
  width: 100%;
}

#question-form > button {
  font-size: 0.8rem;
  display: block;
  box-sizing: border-box;
  width: 100%;
  border-top: 0.5rem;
  border-bottom: 0.5rem;
}

#answer-form > label {
  display: block;
  font-weight: bold;
}

#answer-form > textarea {
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  display: block;
  box-sizing: border-box;
  width: 100%;
}

#answer-form > button {
  font-size: 0.8rem;
  display: block;
  box-sizing: border-box;
  width: 100%;
  border-top: 0.5rem;
  border-bottom: 0.5rem;
}

.bid-window {
  position: absolute;
  z-index: 10;

  /* top: 0; */

  box-sizing: border-box;
  width: 18rem;
  background-color: white;
  border-radius: 0.5rem;
  padding: 1rem 2rem;

  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

#bid-form .label {
  color: black;
  display: block;
}

#bid-form .bid-price {
  margin-top: 2rem;
  margin-bottom: 2rem;
  font-size: 3rem;
  display: flex;
  flex-direction: row;
  align-items: baseline;
}

#bid-form input {
  font-size: inherit;
  width: 100%;
  text-align: right;
  flex-basis: 1;
  flex-grow: 1;
}

#bid-form button {
  width: 100%;
}
</style>
