import { useState, useEffect } from 'react'

const PeriodForm = () => {
  const [periods, setPeriods] = useState([])

  const [formData, setFormData] = useState({
    start_date: '',
    end_date: '',
    vacation_start: '',
    vacation_end: '',
    year: ''

  })

  const handleCreateOrUpdatePeriods = async event => {
    event.preventDefault()

    const url = editPeriodsId
      ? `http://127.0.0.1:8000/periods/${editPeriodsId}`
      : 'http://127.0.0.1:8000/periods/'
    const method = editPeriodsId ? 'PUT' : 'POST'

    const response = await fetch(url, {
      method,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      alert(
        editPeriodsId
          ? 'Ciclo lectivo actualizado exitosamente!'
          : 'Ciclo lectivo exitosamente!'
      )
      fetchGroups()
      setFormData({ name: '' })
      setEditGroupId(null)
    } else {
      alert('No se pudo crear/actualizar el curso')
    }
  }

  const handleDeleteGroup = async id_group => {
    const response = await fetch(`http://127.0.0.1:8000/groups/${id_group}`, {
      method: 'DELETE'
    })

    if (response.ok) {
      alert('¡Curso eliminado exitosamente!')
      fetchGroups()
    } else {
      alert('No se pudo eliminar el curso')
    }
  }
}