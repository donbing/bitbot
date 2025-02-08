import requests
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image

def get_noaa_tide_data(station_id):
#     date = datetime.date.today().strftime("%Y-%m-%d")

#     # Using NOAA Tides & Currents API
#     # station_id = '9414290'  # Example station ID for San Francisco
#     api_url = f"https://environment.data.gov.uk/flood-monitoring/id/stations/{station_id}/readings?_sorted&date={date}"
# response = requests.get(api_url)
#         response.raise_for_status()  # Raise an exception for bad status codes
#         data = response.json()

    url = f'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?product=predictions&application=NOS.COOPS.TAC.WL&begin_date={datetime.now().strftime("%Y%m%d")}&range=168&datum=MLLW&station={station_id}&time_zone=lst_ldt&units=metric&interval=h&format=json'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        tide_data = []
        for prediction in data['predictions']:
            tide_data.append({
                'date': prediction['t'],
                'height': float(prediction['v'])
            })
        return tide_data
    except Exception as e:
        print(f"Error fetching tide data: {e}")
        return []

def render_tide_chart(location_id, img_buf):
    tide_data = get_noaa_tide_data(location_id)
    
    from datetime import datetime
    dates = [datetime.strptime(d['date'], '%Y-%m-%d %H:%M') for d in tide_data]
    heights = [d['height'] for d in tide_data]
    
    plt.figure(figsize=(4, 3))
    plt.plot(dates, heights)
    plt.title('Next 7 Days')
    plt.grid(True)
    
    # Rotate and space out date labels
    import matplotlib.dates as mdates
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().set_xlim(dates[0], dates[-1])
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(7))  # Exactly 7 labels
    
    # Find daily min and max 
    daily_min_max = {}
    day_counts = {}
    for date, height in zip(dates, heights):
        day = date.strftime('%Y-%m-%d')
        if day not in day_counts:
            day_counts[day] = 1
        else:
            day_counts[day] += 1

    for date, height in zip(dates, heights):
        day = date.strftime('%Y-%m-%d')
        if day_counts[day] == 24:  # Only consider days with 24 data points
            if day not in daily_min_max:
                daily_min_max[day] = {'min': (date, height), 'max': (date, height)}
            else:
                if height < daily_min_max[day]['min'][1]:
                    daily_min_max[day]['min'] = (date, height)
                if height > daily_min_max[day]['max'][1]:
                    daily_min_max[day]['max'] = (date, height)

    # Add labels for min and max
    for day, values in daily_min_max.items():
        # Label for minimum
        plt.annotate(
            f"{values['min'][0].strftime('%-I:%p')}",
            xy=(values['min'][0], values['min'][1]),
            xytext=(-15, 0),
            textcoords='offset points',
            ha='center',
            fontsize=8,
            color='red'
        )
        # Label for maximum
        plt.annotate(
            f"{values['max'][0].strftime('%-I:%p')}",
            xy=(values['max'][0], values['max'][1]),
            xytext=(14, 0),
            textcoords='offset points',
            ha='center',
            fontsize=8,
            color='blue'
        )

    plt.tight_layout()

    plt.savefig(img_buf, format='png', dpi=100, bbox_inches='tight')
    plt.close()

    img = Image.open(img_buf)

    return img









