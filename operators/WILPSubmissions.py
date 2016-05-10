from .APIBase import APIBase;
import os;
import pickle;

class WILPSubmissions(APIBase):
    def __init__(self, configuration):
        self.config = configuration;

        headers = {};
        headers['accept'] = self.config["accept"];
        headers['authorization'] = "Bearer " + self.config["authorization"];
        headers['content-type'] = self.config["contenttype"];
        headers['Cache-Control'] = "no-cache";
        configuration['headers'] = headers;
        super(WILPSubmissions, self).__init__(configuration);

        self.fieldMappings = {
            'first': {'name': '<field id>', 'birthday': '<field id>',
                      'gender': '<field id>', 'grade': '<field id>',
                      'feepaid': '<field id>', 'status': '<field id>', 'comments': '<field id>'
                      },

            'second': {'name': '<field id>', 'birthday': '<field id>',
                       'gender': '<field id>', 'grade': '<field id>',
                       'feepaid': '<field id>', 'status': '<field id>', 'comments': '<field id>'
                       },

            'third': {'name': '<field id>', 'birthday': '<field id>',
                      'gender': '<field id>', 'grade': '<field id>',
                      'feepaid': '<field id>', 'status': '<field id>', 'comments': '<field id>'
                      },
            'fourth': {'name': '<field id>', 'birthday': '<field id>',
                      'gender': '<field id>', 'grade': '<field id>',
                      'feepaid': '<field id>', 'status': '<field id>', 'comments': '<field id>'
                      },
            'fifth': {'name': '<field id>', 'birthday': '<field id>',
                      'gender': '<field id>', 'grade': '<field id>',
                      'feepaid': '<field id>', 'status': '<field id>', 'comments': '<field id>'
                      },
            'father':
                {
                    'cellphone': '<field id>',
                    'email': '<field id>',
                    'firstname': '<field id>',
                    'lastname': '<field id>',

                },

            'mother':
                {
                    'cellphone': '<field id>',
                    'email': '<field id>',
                    'firstname': '<field id>',
                    'lastname': '<field id>',

                },

            'misc':
                {
                    'address': '<field id>',
                    'assistance': '<field id>',
                    'allergy': '<field id>',
                    'timestamp': 'timestamp',
                    'primarycontact' : '<field id>',
                    'pickupname' : '<field id>',
                    'pickuprelation' : '<field id>'
                }
        };

    def getData(self):
        print("WILPSubmissions.getData.");
        print(self.config);
        readfile = '';
        if ('file' in self.config):
            print('From File.');
            readfile = self.config['file'];
        else:
            print('From API.');
            result = super(WILPSubmissions, self)._getHttp();
            if('output' in self.config):
                readfile = self.config['output'] + '.bin';
            else:
                import time;
                readfile = 'sysgen-' + time.strftime("%Y%m%d-%H%M%S") + '.bin';

            self._serialize(readfile, result);

        readfile = self._getFilePath(readfile);
        print('Readfile: %s', readfile);
        result = self._deserialize(readfile);

        if('submissions' in result):
            result = result['submissions'];

        if ("output" in self.config):
            return self._createOutput(self.config["output"], result);
        else:
            return result;

    def _createOutput(self, output, jData):
        import csv;
        print("WILPSubmissions._createOutput");
        jData = self._flattenData(jData);
        self._writeToFile(output, str(jData));
        students = self._buildCollection(jData);

        output = self._getFilePath(output, 2) + '.csv';
        with open(output, "w") as csvFile:
            writer = csv.writer(csvFile);
            writer.writerows(students);

        print('CSV written to: ', output);


    def _buildCollection(self, jRows):
        print("WILPSubmissions._buildCollection");
        import copy;
        map = self.fieldMappings;
        childValuesLookupOrder = ['name', 'grade', 'birthday', 'gender', 'status', 'feepaid'];
        csvRows = [['Id', 'Timestamp', 'Father\'s First Name', 'Father\'s Last Name', 'Father\'s Email', 'Father\'s Cell Phone',
                  'Mother\'s First Name', 'Mother\'s Last Name', 'Mother\'s Email', 'Mother\'s Cell Phone',
                  'Address', 'Needs Assistance', 'Allergies', 'Student\'s Name', 'Student\'s Grade', 'Student\'s Birthday',
                  'Student\'s Gender', 'Status', 'Payment', 'Primary Contact', 'Pickup Name', 'Pickup Relation', 'Parents emails']];

        for row in jRows:
            common = [];
            common.append(row['id']);
            common.append(row[self.fieldMappings['misc']['timestamp']]);

            self._addColumnValue(common, row, 'father', 'firstname');
            self._addColumnValue(common, row, 'father', 'lastname');
            self._addColumnValue(common, row, 'father', 'email');
            self._addColumnValue(common, row, 'father', 'cellphone');

            self._addColumnValue(common, row, 'mother', 'firstname');
            self._addColumnValue(common, row, 'mother', 'lastname');
            self._addColumnValue(common, row, 'mother', 'email');
            self._addColumnValue(common, row, 'mother', 'cellphone');

            self._addColumnValue(common, row, 'misc', 'address');
            self._addColumnValue(common, row, 'misc', 'assistance');
            self._addColumnValue(common, row, 'misc', 'allergy');
            parentEmails = None;
            father = self._getValue(row, 'father', 'email', '');
            mother = self._getValue(row, 'mother', 'email', '');

            if((father and mother) and (father.lower() == mother.lower())):
                parentEmails = father;
            else:
                parentEmails = father + '\n' + mother;

            #first child
            firstChild = copy.deepcopy(common);
            secondChild = None;
            thirdChild = None;
            fourthChild = None;
            fifthChild = None;

            for key in childValuesLookupOrder:
                self._addColumnValue(firstChild, row, 'first', key);
            self._addColumnValue(firstChild, row, 'misc', 'primarycontact');
            self._addColumnValue(firstChild, row, 'misc', 'pickupname');
            self._addColumnValue(firstChild, row, 'misc', 'pickuprelation');
            firstChild.append(parentEmails);
            csvRows.append(firstChild);

            #if child two is there
            if(self.fieldMappings['second']['name'] in row and row[self.fieldMappings['second']['name']]['value']):
                secondChild = copy.deepcopy(common);
                secondChild[0] = row['id'] + '01';
                for key in childValuesLookupOrder:
                    self._addColumnValue(secondChild, row, 'second', key);
               
            # if child three is there
            if (self.fieldMappings['third']['name'] in row and row[self.fieldMappings['third']['name']]['value']):
                thirdChild = copy.deepcopy(common);
                thirdChild[0] = row['id'] + '02';
                for key in childValuesLookupOrder:
                    self._addColumnValue(thirdChild, row, 'third', key);
                
            # if child three is there
            if (self.fieldMappings['fourth']['name'] in row and row[self.fieldMappings['fourth']['name']]['value']):
                fourthChild = copy.deepcopy(common);
                fourthChild[0] = row['id'] + '03';
                for key in childValuesLookupOrder:
                    self._addColumnValue(fourthChild, row, 'fourth', key);
                
            # if child three is there
            if (self.fieldMappings['fifth']['name'] in row and row[self.fieldMappings['fifth']['name']]['value']):
                fifthChild = copy.deepcopy(common);
                fifthChild[0] = row['id'] + '04';
                for key in childValuesLookupOrder:
                    self._addColumnValue(fifthChild, row, 'fifth', key);
                
            if(secondChild):
                self._addColumnValue(secondChild, row, 'misc', 'primarycontact');
                self._addColumnValue(secondChild, row, 'misc', 'pickupname');
                self._addColumnValue(secondChild, row, 'misc', 'pickuprelation');
                secondChild.append(parentEmails);
                csvRows.append(secondChild);

            if(thirdChild):
                self._addColumnValue(thirdChild, row, 'misc', 'primarycontact');
                self._addColumnValue(thirdChild, row, 'misc', 'pickupname');
                self._addColumnValue(thirdChild, row, 'misc', 'pickuprelation');
                thirdChild.append(parentEmails);
                csvRows.append(thirdChild);

            if(fourthChild):
                self._addColumnValue(fourthChild, row, 'misc', 'primarycontact');
                self._addColumnValue(fourthChild, row, 'misc', 'pickupname');
                self._addColumnValue(fourthChild, row, 'misc', 'pickuprelation');
                fourthChild.append(parentEmails);
                csvRows.append(fourthChild);

            if(fifthChild):
                self._addColumnValue(fifthChild, row, 'misc', 'primarycontact');
                self._addColumnValue(fifthChild, row, 'misc', 'pickupname');
                self._addColumnValue(fifthChild, row, 'misc', 'pickuprelation');
                fifthChild.append(parentEmails);
                csvRows.append(fifthChild);
        #for loop

        return csvRows;



    def _addColumnValue(self, csvRow, row, cat, fld):
        value = '';
        try:
            if(self.fieldMappings[cat][fld] in row):
                value = self._getValue(row, cat, fld);
                if(fld == 'address'):
                    value = value.replace('\n', '').replace('address = ', '').replace('address2 = ', '').replace('city = ', ', ').replace('state = ', ', ').replace('zip = ', '');
                if(fld != 'email'):
                    value = value.title();
        except Exception:
            pass;
        csvRow.append(value);
        return csvRow;

    def _getValue(self, row, cat, fld, defaultValue = None):
        value = defaultValue;
        if (self.fieldMappings[cat][fld] in row):
            value = row[self.fieldMappings[cat][fld]]['value'];
        return value;

    def _flattenData(self, rows):
        #print('WILPSubmissions._flattenData');
        for row in rows:
            data = row["data"];
            row["data"] = None;
            for fld in data:
                row[fld] = data[fld];
        return rows;

    def _writeToFile(self, filename, content, state=0):
        prefix = 'raw';
        if (state == 1):
            prefix = 'processed';
        if (state == 2):
            prefix = 'final'

        prefix = 'workspace/' + prefix;

        if (not os.path.exists(prefix)):
            os.makedirs(prefix);

        prefix = prefix + '/' + filename;
        f = open(prefix, 'w');
        f.write(content);
        f.close();

    def _serialize(self, filename, object, state=0):
        path = self._getFilePath(filename, state);
        with open(path, 'wb') as f:
            pickle.dump(object, f);

    def _deserialize(self, fqn):
        with open(fqn, 'rb') as f:
            return pickle.load(f);

    def _getFilePath(self, filename, state=0):
        path = 'raw';
        if (state == 1):
            path = 'processed';
        if (state == 2):
            path = 'final'

        path = 'workspace/' + path;

        if (not os.path.exists(path)):
            os.makedirs(path);

        path = path + '/' + filename;
        return path;
