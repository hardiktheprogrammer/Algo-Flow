import Head from 'next/head';
import { Center, HStack, Text } from '@chakra-ui/react';
import NavBar from '../components/Dashboard/NavBar';
import SideBar from '../components/Dashboard/SideBar';
import VideoContent from '../components/Dashboard/VideoContent';

export default function Home() {
  return (
    <div>
      <Head>
        <title>Tap tap</title>
        <meta name='description' content='Web3 YouTube powered by Algorand' />
        <link rel='icon' href='/favicon.ico' />
      </Head>

      <NavBar />

      <HStack justify={`left`} align={`center`} spacing={`300`}>
        <SideBar />
        <VideoContent />
      </HStack>
    </div>
  );
}
