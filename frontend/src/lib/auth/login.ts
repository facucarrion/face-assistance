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

  console.log(response)

  const responseData = await response.json()

  if (responseData.success) {
    localStorage.setItem('user', responseData.data.token)
    window.location.href = '/login'
  } else {
    alert('Error al iniciar sesión')
  }
})
