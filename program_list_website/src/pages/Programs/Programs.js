import React, { useState, useEffect } from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';

async function getPrograms() {
  return fetch(`http://localhost:4002/programs`, { meTableCellod: 'GET' }).then((response) =>
    response.json()
  );
}

const Programs = () => {
  const [programs, setPrograms] = useState(null);
  useEffect(() => {
    async function loadPeople() {
      const programs = await getPrograms();
      setPrograms(programs);
    }
    loadPeople();
  }, []);

  if (!programs) {
    return <div>Loading</div>;
  }

  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell component="th">Name</TableCell>
            <TableCell component="th">Cashback</TableCell>
            <TableCell component="th">Threshold</TableCell>
            <TableCell component="th">Status</TableCell>
            <TableCell component="th">Pause Date</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {programs.map((program) => (
            <tr key={program.id}>
              <TableCell>{program.name}</TableCell>
              <TableCell>{program.return_percentage}</TableCell>
              <TableCell>{program.threshold}</TableCell>
              <TableCell>{program.status}</TableCell>
              <TableCell>{program.pause_at}</TableCell>
            </tr>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default Programs;
