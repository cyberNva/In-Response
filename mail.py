import win32com.client
import pythoncom

class Handler_Class(object):
    def OnNewMailEx(self, receivedItemsIDs):
        try:
            for ID in receivedItemsIDs.split(","):
                mail = outlook.Session.GetItemFromID(ID)
                print("New email received:")
                print("Subject: ", mail.Subject)
                print("Body: ", mail.Body)
        except Exception as e:
            print("Error: ", e)

if __name__ == '__main__':
    
    outlook = win32com.client.DispatchWithEvents("Outlook.Application", Handler_Class)

    # infinite loop to keep the script running
    print("Listening for new emails...")
    pythoncom.PumpMessages()

