''' Search Engine Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
import apps.tableWidget as tW

# List the name, licence_no, addr, birthday, driving class,
# driving_condition, and the expiring_data of a driver by entering either 
# a licence_no or a given name. It shall display all the entries if a
# duplicate name is given.
def searchOne( userCx, strVar, isLicNo ):
        # Check if user input is empty
        if len( strVar ) < 1:
            type = "licence_no" if isLicNo else "Name"
            tm.showerror( "Invalid Input", "You need to specifiy a " +\
                          type + " to search!\nErr 0xa5-2" )
            return
           
        # create the search title for the frame
        title = "licence_no" if isLicNo else "Name"
        title += " search on '" + strVar.lower() + "'"
        
        # build the SQL statement based on if it's a LicNo or a Name
        if isLicNo:
            statement = "SELECT P.name, L.licence_no, P.addr, P.birthday, L.class, L.expiring_date " +\
                        "FROM People P LEFT JOIN drive_Licence L ON P.sin = L.sin "+\
                        "WHERE LOWER(L.licence_no) = " + "'" + strVar.lower() + "'"
        else:
            statement = "SELECT P.name, L.licence_no, P.addr, P.birthday, L.class, L.expiring_date " +\
                        "FROM People P LEFT JOIN drive_Licence L ON P.sin = L.sin "+\
                        "WHERE LOWER(P.name) = " + "'" + strVar.lower() + "'"
            
        #print( statement )
        thisCursor = userCx.cursor()
        
        # try to execute the requested statement
        try:
            thisCursor.execute( statement )
        except:
            # NEED TO INCLUDE HELP FOR DETERMINING ERRORS IN THE SQL STATEMENT
            tm.showerror( "Invalid Input", "There is a problem with your search, please try again.\nErr 0xa5-3" )
            return
         
        rows = thisCursor.fetchall()
        
        if len( rows ) == 0:
            infoMsg = title + " produced no results!"
            tm.showinfo( "No results!", infoMsg )
            return
    
        # build the tableSpace for tableWidget =================================
        numRows = len( rows )
        numCols = len( thisCursor.description )
        
        # get the header elements
        headerList = []
        for object in thisCursor.description:
            headerList.append( object[0] )
        # append the extra search for conditions
        headerList.append( "CONDITION(S)" )
        
        # start the tableSpace with the header row
        tableRows = [headerList]
        
        # loop through all the rows returned by fetchall
        for x in range( numRows ):
            tempRow = []
            for entry in rows[x]:
                # for every entry in each row, append it to the temporary row
                if entry == None:
                    # if entry is a NoneType, apply this value instead
                    tempRow.append( "N/A" )
                else:
                    tempRow.append( entry )
            # When a temporary row is complete, search for the conditions on that result
            # Because of the LEFT JOIN, some licence may be NoneType
            if tempRow[1] == "N/A":
                tempRow.append( "N/A" )
                tableRows.append( tempRow )
                continue;
            statement = "SELECT DC.description " +\
                         "FROM restriction R, driving_condition DC " +\
                        "WHERE R.r_id = DC.c_id AND LOWER(R.licence_no) = '" + tempRow[1].strip().lower() + "'"
            thisCursor.execute( statement )  
            conditions = thisCursor.fetchall()
            if len( rows ) == 0:
                # if no conditions found for the licence, append N/A value
                tempRow.append( "N/A" )
            else:
                # if conditions found, append them the final element of tempRow
                condStr = ""
                #print( conditions )
                for object in conditions:
                    condStr += object[0] + "\n"
                # take all but the last newline character of the condStr
                tempRow.append( condStr[ 0: len(condStr)-1 ] )
                    
            tableRows.append( tempRow )
        
        #print( tableRows )
        
        tW.buildCxTable( tableRows, title )

def run( userCx ):
    # prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa5-1" )
        return
    
    top = Tk()
    top.title( "app5: Search Engine" )

    # LIST1 ====================================================================
    info1 = "entering either a licence_no or a given name."
    msg1 = Message( top, text=info1, padx=5, pady=5, width=200 )
    msg1.grid( row=0, sticky=N, columnspan=2 )

    name_entry = Entry( top )
    name_entry.grid( row=1, column=0, sticky=EW )
    name_entry.insert( 0, "Enter a name here")
    
    licNo_entry = Entry( top )
    licNo_entry.grid( row=1, column=1, sticky=EW )
    licNo_entry.insert( 0, "Enter a licence_no here" )
    
    search1Name_button = Button( top, text="Search By Name", command=lambda: searchOne( userCx, name_entry.get(), False ) )
    search1Name_button.grid( row=2, column=0, sticky=EW )
    
    search1LicNo_button = Button( top, text="Search By licence_no", command=lambda: searchOne( userCx, licNo_entry.get(), True ) )
    search1LicNo_button.grid( row=2, column=1, sticky=EW )

    
    # LIST2 ====================================================================
    info2 = "drive licence_no or sin of a person  is entered."
    msg2 = Message( top, text=info2, padx=5, pady=5, width=200 )
    msg2.grid( row=3, sticky=N, columnspan=2 )

    sin_entry = Entry( top )
    sin_entry.grid( row=4, column=0, sticky=EW )
    sin_entry.insert( 0, "Enter a SIN here" )
    
    # NOTICE THE NAME... I SUCK AT NAMING HELP
    lic_entry = Entry( top )
    lic_entry.grid( row=4, column=1, sticky=EW )
    lic_entry.insert( 0, "Enter a licence_no here" )

    search2Name_button = Button( top, text="Search By SIN", command=lambda: searchTwo( userCx, sin_entry.get(), False ) )
    search2Name_button.grid( row=5, column=0, sticky=EW )
    
    search2LicNo_button = Button( top, text="Search By licence_no", command=lambda: searchTwo( userCx, lic_entry.get(), True ) )
    search2LicNo_button.grid( row=5, column=1, sticky=EW )
    
    mainloop()

    # LIST3 ====================================================================
    info3 = "entering the vehicle's serial number."
    msg3 = Message( top, text=info3, padx=5, pady=5 )
    msg3.pack()

    strVar3 = StringVar()
    strVar3.set( "Enter a VIN" )
    entry3 = Entry( top, textvariable=strVar3 )
    entry3.pack()

    # Perform the search for 
    def list3():
        print( strVar3.get() )

    button3 = Button( top, text="Search Vehicle History", command=list3 )
    button3.pack()

    #mainloop
    mainloop()