import { writable } from 'svelte/store';
import type { Writable } from 'svelte/store';

export interface CartItem {
  id: number;
  service_id: number;
  service_name: string;
  price: number;
  quantity: number;
  billing_period: string;
  subtotal: number;
}

export interface CartState {
  items: CartItem[];
  total: number;
  itemCount: number;
}

function createCartStore(): Writable<CartState> {
  const { subscribe, set, update } = writable<CartState>({
    items: [],
    total: 0,
    itemCount: 0,
  });

  return {
    subscribe,
    addItem: (item: CartItem) => {
      update((state) => {
        const existing = state.items.find((i) => i.service_id === item.service_id);
        if (existing) {
          existing.quantity += item.quantity;
          existing.subtotal = existing.price * existing.quantity;
        } else {
          state.items.push(item);
        }
        const total = state.items.reduce((sum, i) => sum + i.subtotal, 0);
        return {
          ...state,
          total,
          itemCount: state.items.reduce((sum, i) => sum + i.quantity, 0),
        };
      });
    },
    removeItem: (serviceId: number) => {
      update((state) => {
        state.items = state.items.filter((i) => i.service_id !== serviceId);
        const total = state.items.reduce((sum, i) => sum + i.subtotal, 0);
        return {
          ...state,
          total,
          itemCount: state.items.reduce((sum, i) => sum + i.quantity, 0),
        };
      });
    },
    updateQuantity: (serviceId: number, quantity: number) => {
      update((state) => {
        const item = state.items.find((i) => i.service_id === serviceId);
        if (item) {
          item.quantity = quantity;
          item.subtotal = item.price * quantity;
        }
        const total = state.items.reduce((sum, i) => sum + i.subtotal, 0);
        return {
          ...state,
          total,
          itemCount: state.items.reduce((sum, i) => sum + i.quantity, 0),
        };
      });
    },
    clear: () => {
      set({ items: [], total: 0, itemCount: 0 });
    },
  };
}

export const cartStore = createCartStore();
