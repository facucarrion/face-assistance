import { userToken } from '../../stores/tokenStore'

export const logOut = () => {
  localStorage.removeItem('user')
  userToken.set(null)
  window.location.reload()
}
