# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import calendar

def days360(start_date, end_date, method_eu=False):

	start_day = start_date.day
	start_month = start_date.month
	start_year = start_date.year
	end_day = end_date.day
	end_month = end_date.month
	end_year = end_date.year

	if (
		start_day == 31 or
		(
			method_eu is False and
			start_month == 2 and (
				start_day == 29 or (
					start_day == 28 and
					calendar.isleap(start_year) is False
				)
			)
		)
	):
		start_day = 30

	if end_day == 31:
		if method_eu is False and start_day != 30:
			end_day = 1

			if end_month == 12:
				end_year += 1
				end_month = 1
			else:
				end_month += 1
		else:
			end_day = 30

	return (
		end_day + end_month * 30 + end_year * 360 -
		start_day - start_month * 30 - start_year * 360)


def float_2_time(time):

	# import datetime
	# td = datetime.timedelta(hours = float(time))
	# print (datetime.datetime(2000, 1, 1) + td).strftime("%H:%M")

	seconds = float(time)*3600
	minutes, seconds = divmod(seconds, 60)
	hours, minutes = divmod(minutes, 60)

	print "%02d:%02d:%02d"%(hours, minutes, seconds)


def month_30days(month_start, month_end, actual_days):
	from datetime import datetime
	start_date = datetime.strptime(month_start, "%d-%m-%Y")
	end_date = datetime.strptime(month_end, "%d-%m-%Y")

	working_days = (end_date - start_date).days + 1
	if working_days == actual_days:
		return 30
	else:
		diff_days = (working_days - 30)
		if (working_days - abs(diff_days)) > actual_days:
			diff_days = 0
		
		return actual_days - diff_days