export interface Order {
  id: string
  status: 'pending' | 'paid' | 'cancelled'
}

export function canCancel(order: Order): boolean {
  return order.status === 'pending'
}
