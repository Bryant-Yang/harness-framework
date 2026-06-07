import { canCancel, type Order } from '../domain/order'

export function getOrderActions(order: Order): string[] {
  return canCancel(order) ? ['cancel'] : []
}
