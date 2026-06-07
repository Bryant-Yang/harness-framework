import { canCancel, type Order } from '../domain/order'

export function serializeOrder(order: Order) {
  return {
    id: order.id,
    cancellable: canCancel(order),
  }
}
