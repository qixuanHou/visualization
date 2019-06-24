package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.io.IntWritable;

import java.io.IOException;
import java.util.StringTokenizer;
import java.util.*;

public class Q4 {

  public static class theMapOne extends Mapper<Object, Text, Text, IntWritable> {
    private Text source = new Text();
    private IntWritable weight = new IntWritable();


    protected void map(Object key, Text value, Context context) throws IOException, InterruptedException {

      String line = value.toString();
      StringTokenizer st = new StringTokenizer(line, "\t"); 

      source.set(st.nextToken());
      weight.set(0);
      context.write(source, weight);

      source.set(st.nextToken());
      weight.set(1);
      context.write(source, weight);
    }
  }

  public static class theReducerOne extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

      int out = 0;
      int in = 0;
      for (IntWritable val: values) {
        if (val.get() == 0) {
          out +=1;
        } else {
          in += 1;
        }
      }
      result.set(out-in);
      context.write(key, result);
    }
  }

  public static class theMapperTwo extends Mapper<Object, Text, Text, IntWritable>{

    private Text source = new Text(); 
    private final static IntWritable weight = new IntWritable(1); 

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String line = value.toString();
      StringTokenizer st = new StringTokenizer(line, "\t"); 
      st.nextToken();
      source.set(st.nextToken()); 

      context.write(source, weight);
    }
  }


  public static class theReducerTwo extends Reducer<Text, IntWritable, Text, IntWritable> {

    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {

      int count = 0; 

      for (IntWritable val : values) {
        count +=1;
      }
      result.set(count); 
      context.write(key, result);
    }
  }



  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q4");
    Job job2 = Job.getInstance(conf, "Q4");

    /* TODO: Needs to be implemented */
    job.setJarByClass(Q4.class);
    job.setMapperClass(theMapOne.class);
    job.setReducerClass(theReducerOne.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    job2.setJarByClass(Q4.class);
    job2.setMapperClass(theMapperTwo.class);
    job2.setReducerClass(theReducerTwo.class);
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);


    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1] + "/temp"));
    FileInputFormat.addInputPath(job2, new Path(args[1] + "/temp"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1] + "/final"));
    job.waitForCompletion(true);
    System.exit(job2.waitForCompletion(true) ? 0 : 1);

  }
}
