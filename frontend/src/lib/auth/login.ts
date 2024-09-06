import { userToken } from '../../stores/tokenStore'

const form = document.getElementById('form') as HTMLFormElement

form.addEventListener('submit', async e => {
  e.preventDefault()

  const formData = new FormData(form)
  const data = Object.fromEntries(formData)

  const response = await fetch('http://127.0.0.1:8000/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })

  const responseData = await response.json()

  if (responseData.success) {
    userToken.set(responseData.data.token)
    location.href = '/'
  } else {
    alert('Error al iniciar sesión')
  }
})
