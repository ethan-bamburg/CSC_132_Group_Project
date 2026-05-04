from math import e #Importing euler's number is needed for the equations



#I decided a class would be useful to keep variables organized and reduce bloat.
class Ambiance():
    def __init__(self, relative_humidity:float, temperature:float, windspeed:float):
        self.relative_humidity = relative_humidity
        self.temperature = temperature
        self.windspeed = windspeed

    #RH is a percentage, so it is bound between 0 and 100. It shouldn't ever reach 0, though, because that's impossible and would throw off equations.
    #RH will rarely go below 10% in real, non-experimental, indoor conditions. And if it does, there are different equations for extreme weather that a desk fan probably won't be relevant to.
    @property
    def relative_humidity(self):
        return self._relative_humidity
    @relative_humidity.setter
    def relative_humidity(self, relative_humidity):
        if relative_humidity > 100:
            self._relative_humidity = 100
        elif relative_humidity <=10:
            self._relative_humidity = 10
        else:
            self._relative_humidity = relative_humidity

    #Temperature is technically not limited, but it will be in this case to prevent anything too egregious should sensors give an error
    @property
    def temperature(self):
        return self._temperature
    @temperature.setter
    def temperature(self, temperature):
        if temperature> 50:
            self._temperature = 50
        elif temperature < -40:
            self._temperature = -40
        else:
            self._temperature = temperature

    #As far as I know, windspeed will not normally register as negative when using our sensor. Message me if it does so that I can update this!
    @property
    def windspeed(self):
        return self._windspeed
    @windspeed.setter
    def windspeed(self, windspeed):
        if windspeed < 0:
            self._windspeed = 0
        else:
            self._windspeed = windspeed


            #Important notes for temperature methods:
    """Temperature is always measured in Celsius for these equations. When measuring temperature,
the thermometer should be well-sheltered so that environmental moisture, wind, or other
disruptions don't register twice -- once in the thermometer, and once in the equations themselves.
We could consider wrapping the thermometer in a thin plastic wrap or shell."""


    """Update functions are probably what will be used most, so they're at the top.
    Changes the value of a certain parameter in Ambiance. They would be all one function,
    but that would lead to some redundancy and slowdown if the different separated sensors each
    updated all the values at once."""

    def updateRH(self, relative_humidity:float):
        self.relative_humidity = relative_humidity

    def updateTemperature(self, temperature:float):
        self.temperature = temperature

    def updateWind(self,windspeed:float):
        self.updateWind = windspeed


    """This equation accounts for the specifics of how humidity 
    affects apparent temperature. Loosely speaking, humidity will make hot weather
    feel hotter, and cold weather feel colder, scaling based on its intensity."""
    #Uses humidity in %, temperature in C.
    def findVaporPressure(self)->float:     
        return 6.105 * (0.01*self.relative_humidity) * e*(17.27*self.temperature/(237.7+self.temperature))


    """Windspeed must be in meters per second. Typically, this is measured 10 meters above ground or sea level.
    However, we are usually providing the wind (via the fan), and are situated indoors, so it is less relevant 
    but included for accuracy's sake"""
    #Returns what the temperature "should" feel like when accounting for humidity, windspeed, and actual temperature.
    def findFeelsLike(self)->float:
        p = self.findVaporPressure()
        return self.temperature + 0.33 * p - (0.7 * self.windspeed) - 4.00

    #Version of findFeelsLike that does not use windspeed, used for calculateWindAdjustment
    def findFeelsLikeNoWind(self)->float:
        p = self.findVaporPressure()
        return self.temperature * 0.33 * p - 4.0

    """Accepts a desired temperature, the current absolute temperature, and other metrics, and returns the
    windspeed needed to change the absolute temperature into the desired one. The process of finding 
    how much RPM equals a certain speed of wind, along with the rate at which the fan adjusts
    to new speeds, will both be done later when physical equipment is more ready."""
    #If desired temp is hotter than or equal to the current absolute temperature, returns 0.
    def calculateWindAdjustment(self, desiredtemp)->float:
        if desiredtemp >= self.temperature:
            return 0
        apparent_temp_no_wind = self.findFeelsLikeNoWind()
        return 0.7*(apparent_temp_no_wind-desiredtemp)
    

    

    #TODO: A __str__ function will be added once the GUI is more fleshed out.


#Functions for basic conversions. Could be integrated better once other aspects of project are more fleshed out.
def celsius(F:float)->float:
    return (F-32)*(5/9)

def fahrenheit(C:float)->float:
    return C*(9/5)+32

def mphToMs(mph:float)->float:
    return mph/2.237



#Finally, a bit of code for testing this file.
if __name__ == "__main__":
    rh = float(input("Input a relative humidity percentage as a percentage number. "))
    temp = float(input("Input an absolute temperature in Celsius. "))
    wind = float(input("Input a wind speed in meters per second. "))

    a = Ambiance(rh, temp, wind)
    print(f"It would feel like {a.findFeelsLike()}C with a temperature of {a.temperature}C, windspeed of {a.windspeed}m/s, and relative humidity of {a.relative_humidity}%.")
    print(f"This is equivalent to a temperature of {fahrenheit(a.temperature)}F and a windspeed of {mphToMs(a.windspeed)} MPH.")
    desired = float(input("What is the temperature you want these conditions to feel like? "))
    print(f"To feel like {desired}C on a day like this, you would need a windspeed of {a.calculateWindAdjustment(desired)}m/s.")
    print(f"Or, in American, to feel like {fahrenheit(desired)}F, you would need a windspeed of {mphToMs(a.calculateWindAdjustment(desired))} MPH.")