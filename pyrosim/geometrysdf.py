from pyrosim.commonFunctions import Save_Whitespace

class GEOMETRY_SDF: 

    def __init__(self,size, objectType):

        self.objectType = objectType

        self.depth   = 4

        self.string1 = '<geometry>'

        if objectType == 'box':

            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])

            self.string2 = ' <box>'

            self.string3 = ' <size>' + sizeString + '</size>'

            self.string4 = ' </box>'

            self.string5 = '</geometry>'
        
        elif objectType == 'sphere':
                
            radString = str(size[0])

            self.string2 = ' <sphere>'

            self.string3 = ' <radius>' + radString + '</radius>'

            self.string4 = ' </sphere>'

            self.string5 = '</geometry>'
            
        else:
            lenString = str(size[0])
            radString = str(size[1])

            self.string2 = ' <cylinder>'

            self.string3 = ' <length>' + lenString + '</length>'

            self.string4 = ' <radius>' + radString + '</radius>'

            self.string5 = ' </cylinder>'

            self.string6 = '</geometry>'
            # return f'Error: Unknown geometry type {objectType}.'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string4 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string5 + '\n' )

        if self.objectType == 'cylinder':
                
                Save_Whitespace(self.depth,f)
    
                f.write( self.string6 + '\n' )