import sysv_ipc
import socket

QUEUE_KEY = 5678
mq = None

try:
	mq = sysv_ipc.MessageQueue(QUEUE_KEY)
	print "Found mq"

except Exception as e:

	print "no Found mq: {}".format(e)


def send(event):
	"""
	Send hostname and Printer Status to Kaa SDK.
	:param msg:
	:return:
	"""

	id = get_hostname()

	message = str(id) + "|" + str(event)

	if mq is None:  # if no mq exists
		print "mq is None"

	else:  # if mq exists
		try:

			mq.send(message)
			print 'completed sending message'

		except Exception as e:

			print 'failed to send message: {}'.format(e)


def get_hostname():
	"""
	Get Raspberry pi hostname.
	:return:
	"""
	hostname = socket.gethostname()

	return hostname
