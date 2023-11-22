export const HOST = (() => {
  if (import.meta.env.DEV) {
    // If in development, use the django server address
    return "http://localhost:8000";
  } else {
    // Otherwise, use the current host
    return "";
  }
})();

interface XMLData {
  [key: string]: number | string | File | undefined;
}

function objectToFormData(params: XMLData) {
  const form = new FormData();

  for (let key in params) {
    let value = params[key];
    if (typeof value === 'number') {
      value = value.toString();
    } else if (value === undefined) {
      continue;
    }
    form.append(key, value);
  }

  return form;
}

export interface ServerResponse {
  status: 'OK' | 'FAILED';
  message?: string;
  value?: any;
}

export async function get(endpoint: string, query?: Record<string, string>): Promise<any> {
  if (!endpoint.endsWith('/')) endpoint += '/';
  if (query) {
    const params = new URLSearchParams(query);
    endpoint = `${endpoint}?${params.toString()}`;
  }
  const res = await fetch(`${HOST}/api${endpoint}`, { credentials: "include" });
  const json: ServerResponse = await res.json();
  if (json.status !== 'OK') throw json.message;
  return json.value;
}

export async function post(endpoint: string, body: XMLData): Promise<any> {
  if (!endpoint.endsWith('/')) endpoint += '/';
  const res = await fetch(`${HOST}/api${endpoint}`, {
    method: 'POST',
    body: objectToFormData(body),
    credentials: "include",
  });
  const json: ServerResponse = await res.json();
  if (json.status !== 'OK') throw json.message;
  return json.value;
}

export async function put(endpoint: string, body: XMLData): Promise<any> {
  if (!endpoint.endsWith('/')) endpoint += '/';
  const res = await fetch(`${HOST}/api${endpoint}`, {
    method: 'PUT',
    body: objectToFormData(body),
    credentials: "include",
  });
  const json: ServerResponse = await res.json();
  if (json.status !== 'OK') throw json.message;
  return json.value;
}

export interface Item {
  id: number;
  owner: User;
  title: string;
  desc: string;
  photo_path: string;
  // NOTE: Prices are returned as strings
  // You must use "parseFloat" to parse it into a number
  starting_price: string;
  bid_price: string;
  bid_user: User;
  end_date: string;
  // the price to be displayed publicly
  current_price: string;
  // whether this item has any bids
  has_bids: boolean;
  // whether this item's auction has ended
  has_ended: boolean;
}

/** Get a list of all items */
export async function getItems(query?: string): Promise<Item[]> {
  if (query) {
    return await get('/items', { q: query });
  } else {
    return await get('/items');
  }
}

/** Get a single item by ID */
export async function getItem(id: number): Promise<Item> {
  return await get(`/items/${id}`);
}

export interface ItemEditParams extends XMLData {
  title: string;
  desc: string;
  photo?: File;
  starting_price: number;
  end_date: string;
  // Owner can't set these:
  // bidPrice: number;
  // bidUser: User;
}

/** Create a single item, and return its data */
export async function createItem(item: ItemEditParams): Promise<Item> {
  return await post('/items', item);
}

/** Update a single item, and return its data */
export async function updateItem(id: number, item: ItemEditParams): Promise<Item> {
  return await put(`/items/${id}`, item);
}

interface ItemBidParams extends XMLData {
  bid_price: number;
}

/** Bid on a single item, and return the updated item data */
export async function bidItem(itemId: number, bid: ItemBidParams): Promise<Item> {
  return await put(`/items/${itemId}/bid`, bid);
}

export interface ItemQuery {
  id: number;
  question: string;
  asked_by: User;
  answer: string | null;
}

export async function getItemQueries(itemId: number): Promise<ItemQuery[]> {
  return await get(`/items/${itemId}/queries`);
}

export async function getItemQuery(itemId: number, queryId: number): Promise<ItemQuery> {
  return await get(`/items/${itemId}/queries/${queryId}`);
}

interface ItemQueryEditParams extends XMLData {
  question: string;
}

export async function createItemQuery(itemId: number, query: ItemQueryEditParams): Promise<ItemQuery> {
  return await post(`/items/${itemId}/queries`, query);
}

export async function updateItemQuery(itemId: number, queryId: number, query: ItemQueryEditParams): Promise<ItemQuery> {
  return await put(`/items/${itemId}/queries/${queryId}`, query);
}

interface ItemQueryAnswerParams extends XMLData {
  answer: string;
}

export async function answerItemQuery(itemId: number, queryId: number, answer: ItemQueryAnswerParams): Promise<ItemQuery> {
  return await put(`/items/${itemId}/queries/${queryId}/answer`, answer);
}

export interface User {
  id: number;
  email: string;
  dob: string;
  avatar_path: string;
}

/** Get a single user by ID */
export async function getUser(userId: number): Promise<User> {
  return await get(`/users/${userId}`);
}

/** Get the currently-logged-in user */
export async function getCurrentUser(): Promise<User> {
  return await get(`/profile`);
}

export interface UserEditParams extends XMLData {
  email: string;
  password: string;
  dob: string;
  avatar?: File;
}

/** Update a single user, and return its data */
export async function updateUser(userId: number, user: UserEditParams): Promise<User> {
  return await put(`/users/${userId}`, user);
}

/** Update the currently-logged-in user, and return its data */
export async function updateCurrentUser(user: UserEditParams): Promise<User> {
  return await put(`/profile`, user);
}
