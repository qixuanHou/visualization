package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.StringTokenizer;
import java.lang.InterruptedException;

public class Q1 {

  public static class theMapper extends Mapper<Object, Text, Text, IntWritable> {
    private Text source = new Text();
    private final static IntWritable weight = new IntWritable(1);

    public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
      String line = value.toString();
      StringTokenizer st = new StringTokenizer(line, "\t");

      st.nextToken();
      source.set(st.nextToken());
      weight.set(Integer.parseInt(st.nextToken()));

      context.write(source, weight);
    }
  }

  public static class theReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    private IntWritable result = new IntWritable();
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
      int sum = 0;
      for (IntWritable val: values) {
        sum += val.get();
      }
      result.set(sum);
      context.write(key, result);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    /* TODO: Needs to be implemented */

    job.setJarByClass(Q1.class);
    job.setMapperClass(theMapper.class);
    job.setCombinerClass(theReducer.class);
    job.setReducerClass(theReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
