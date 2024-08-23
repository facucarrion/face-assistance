import { Doughnut } from 'react-chartjs-2'
import {
  Chart,
  DoughnutController,
  ArcElement,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(DoughnutController, ArcElement, Tooltip, Legend)

export const DoughnutChart = ({ assistance }) => {
  const data = {
    labels: ['Asistidos', 'No asistidos', 'Tarde'],
    datasets: [
      {
        label: 'Asistencia',
        data: [
          assistance.assisted,
          assistance['not-assisted'],
          assistance.late
        ],
        backgroundColor: ['#10B981', '#EF4444', '#F59E0B'],
        borderWidth: 1
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: true,
        text: 'Distribución de Asistencia'
      }
    }
  }

  return (
    <div className='w-1/2'>
      <Doughnut data={data} options={options} />
    </div>
  )
}
